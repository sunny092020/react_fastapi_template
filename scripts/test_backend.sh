#! /usr/bin/env bash

# Exit in case of error
set -e

reset

docker exec -it backend bash -c "pytest $@"
