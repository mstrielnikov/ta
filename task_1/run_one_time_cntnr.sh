#!/bin/sh

if [ ! -f "./scripts/.env" ]
then
  echo "./scripts/.env file with vars doesn't set" && exit 1;
fi

docker run --rm -v "$(pwd)/:/app" -w /app "python:3.13-slim" /bin/bash -c "cd scripts && pip3 install -r requirements.txt && python web3_deploy.py"