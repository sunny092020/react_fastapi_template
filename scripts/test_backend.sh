#! /usr/bin/env bash

# Exit in case of error
set -e

reset
docker-compose run backend pytest $@