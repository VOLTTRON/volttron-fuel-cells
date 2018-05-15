#! /usr/bin/env bash

source ${VOLTTRON_ROOT}/env/bin/activate

python setup-platform.py
PID=$?
echo "the pid is $PID"
if [ "$PID" == "0" ]; then
    volttron -vv
fi
