#!/bin/bash

# Run lint in backend container
docker exec -it backend bash -c "./scripts/lint.sh"

# Run lint in frontend container
docker exec -it frontend bash -c "yarn lint"
