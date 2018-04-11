#!/usr/bin/env bash

PID_FILE="image_pid_file"

# run
if [ "$1" = "stop" ]; then
    pid=$(cat $PID_FILE)
    kill -9 $pid
else
    if [ -f "/usr/local/python-2.7/bin/python" ]; then
        nohup /usr/local/python-2.7/bin/python main_image.py "$@" > nohub.log 2>&1 &
    else
        nohup python main_image.py "$@" > nohub.log 2>&1 &
    fi
    echo $! > $PID_FILE
fi