#!/bin/bash -e

PYTHONHASHSEED=$(python -c 'import random; print(random.randint(1, 4294967295))')
export PYTHONHASHSEED
echo "PYTHONHASHSEED=$PYTHONHASHSEED"

# If no X server is found, we use xvfb to emulate it
if [[ $(uname) == "Linux" && -z $DISPLAY ]]; then
    export DISPLAY=":0"
    XVFB="xvfb-run "
fi

PYTEST_TARGET=tests
PYTEST_CMD="${XVFB}pytest -r fEs -s --cov=src --cov-report=xml --cov-append $PYTEST_TARGET"

echo "$PYTEST_CMD"
sh -c "$PYTEST_CMD"
