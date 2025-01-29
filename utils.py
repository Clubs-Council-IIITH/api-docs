import os
import subprocess
import hashlib
import hmac

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles


def verify_signature(
    payload_body: bytes, secret_token: str | None, signature_header: str
):
    """
    Verify that the payload was sent from GitHub by validating SHA256.

    Args:
        payload_body: original request body to verify (request.body())
        secret_token: GitHub app webhook token (WEBHOOK_SECRET)
        signature_header: header received from GitHub (x-hub-signature-256)
    """
    if not secret_token:
        raise HTTPException(status_code=403, detail="Secret token is missing!")
    if not signature_header:
        raise HTTPException(
            status_code=403, detail="x-hub-signature-256 header is missing!"
        )

    hash_object = hmac.new(
        secret_token.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    if not hmac.compare_digest(expected_signature, signature_header):
        raise HTTPException(status_code=403, detail="Request signatures didn't match!")


def run_build(app, build_dir: str = "/build", services_dir: str = "/services"):
    # Git Clone
    result_git = subprocess.run(
        [
            "git",
            "clone",
            "-j8",
            "--recurse-submodules",
            "--remote-submodules",
            "git@github.com:Clubs-Council-IIITH/services.git",
            services_dir,
        ],
        capture_output=True,
        text=True,
    )

    # print(result_git)
    returncode = result_git.returncode
    stderr = result_git.stderr

    if returncode != 0 and "already exists" in stderr:
        curr_dir = os.getcwd()
        os.chdir(services_dir)

        subprocess.run(
            ["git", "pull", "origin", "master"], capture_output=True, text=True
        )

        result_pull = subprocess.run(
            ["git", "submodule", "update", "--recursive"],
            capture_output=True,
            text=True,
        )

        os.chdir(curr_dir)

        # print(result_pull)
        returncode = result_pull.returncode
        stderr = result_pull.stderr

    if returncode == 0:
        # Run the mkdocs build command
        result = subprocess.run(
            ["mkdocs", "build", "-d", build_dir+"_temp"], capture_output=True, text=True
        )

        # print("Build Result: ", result)

        if result.returncode == 0:
            # Move the new temp to build
            os.system(f"mv {build_dir}_temp/* {build_dir}/")
            os.system(f"rm -rf {build_dir}_temp")
            
            # If the build is successful, remount the static files
            app.router.routes = [
                route
                for route in app.router.routes
                if not (hasattr(route, "name") and route.name == "static")
            ]
            app.mount("/", StaticFiles(directory=build_dir, html=True), name="static")
            return {"message": "Update Successful!!"}
        else:
            # If the build fails, return the error
            print("Build failed: ", result.stderr)
            return JSONResponse(
                content={"error": "Build failed", "details": result.stderr},
                status_code=500,
            )
    else:
        # If the git clone fails, return the error
        print("Git clone failed: ", stderr)
        return JSONResponse(
            content={"error": "Git clone failed", "details": stderr},
            status_code=500,
        )
