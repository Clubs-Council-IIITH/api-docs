#!/bin/sh

# Start the smee client
smee -u https://smee.io/0PaMe47vnB2BFjQQ --target /webhook/ --port 8000 &

# Start the API server
uvicorn main:app --host 0.0.0.0 --port 8000