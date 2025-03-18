#!/bin/sh

docker run --rm -v "$(pwd)":/app -w /app golang:1.24 bash -c "go mod tidy && go run ."

