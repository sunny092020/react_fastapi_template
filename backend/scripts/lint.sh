#!/bin/bash
black . --line-length 120
pycodestyle --max-line-length=120 .
flake8 --max-line-length=120 .
