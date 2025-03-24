#!/bin/sh

if [ ! -f "./.env" ]
then
  echo ".env file with vars doesn't set" && exit 1;
fi

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
fi

if [ -z "$1" ]
  then
    echo "The wallet address as script argument is required"
fi

docker run --rm -v "$(pwd)/:/app" \
  -w /app "python:3.13-slim" /bin/bash \
  -c "pip3 install -r requirements.txt && python main.py block-number && python main.py balance $1"
