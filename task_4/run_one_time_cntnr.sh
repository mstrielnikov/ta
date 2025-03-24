#!/bin/sh

if [ ! -f "./.env" ]
then
  echo ".env file with vars doesn't set" && exit 1;
fi

docker run --rm -v "$(pwd)":/app -w /app -p 8080:8080 golang:1.24 bash -c "go mod tidy && go run ."

#ETH_NODE_URL="https://mainnet.infura.io/v3/*******"
#PORT="8080"
#docker run --rm -v "$(pwd)":/app -w /app -p "$PORT:8080" -e "PORT=$PORT" -e ETH_NODE_URL="$ETH_NODE_URL" golang:1.24 bash -c "go mod tidy && go run ."
