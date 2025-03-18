#!/bin/sh
if [ ! -f "./env" ]
then
  echo ".env file with vars doesn't set" && exit 1;
fi

docker run --rm -v "$(pwd)/:/app" -w /app "python:3.13-slim" /bin/bash -c "pip3 install -r requirements.txt && python main.py"

