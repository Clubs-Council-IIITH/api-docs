from datetime import datetime
import pytz
import subprocess

def get_git_commit(repo_path):
    """Returns the latest Git commit ID from the given repository path."""
    try:
        commit_id = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=repo_path).decode("utf-8").strip()
    except Exception:
        commit_id = "Unknown"
    return commit_id

def define_env(env):
    # get mkdocstrings' Python handler
    python_handler = env.conf["plugins"]["mkdocstrings"].get_handler("python")

    # get the `update_env` method of the Python handler
    update_env = python_handler.update_env

    # override the `update_env` method of the Python handler
    def patched_update_env(config):
        update_env(config=config)

        # get the `convert_markdown` filter of the env
        convert_markdown = python_handler.env.filters["convert_markdown"]

        # build a chimera made of macros+mkdocstrings
        def render_convert(markdown: str, *args, **kwargs):
            return convert_markdown(env.render(markdown), *args, **kwargs)

        # patch the filter
        python_handler.env.filters["convert_markdown"] = render_convert

    # patch the method
    python_handler.update_env = patched_update_env

    timezone = pytz.timezone("Asia/Kolkata")
    env.variables["build_date"] = datetime.now(timezone).strftime(
        "%A, %B %d, %Y at %I:%M %p"
    )

    # Directly access the Python handler's config to get the paths
    # This accesses the actual handler configuration rather than the raw config
    try:
        # Get the handler configuration 
        handler_config = python_handler.config
        if hasattr(handler_config, "paths") and handler_config.paths:
            repo_path = handler_config.paths[0]
        else:
            # Try to access it through attributes if it's a different structure
            repo_path = getattr(handler_config, "paths", ["/app/services"])[0]
    except (AttributeError, IndexError):
        handler_attrs = {attr: getattr(python_handler, attr) for attr in dir(python_handler) 
                        if not attr.startswith('__')}
        env.variables["debug_handler"] = str(handler_attrs)
        repo_path = "/app/services"  # Fallback
    
    env.variables["git_commit"] = get_git_commit(repo_path)
    # env.variables["repo_path"] = repo_path