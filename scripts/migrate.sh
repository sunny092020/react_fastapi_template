#!/bin/bash

set -e

docker-compose run --rm backend alembic upgrade head
