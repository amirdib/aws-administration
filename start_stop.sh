#!/bin/bash

cd /home/ubuntu/instance_administration

if [ $1 = "start" ]; then
    python3 start_stop_instance.py $1
fi

if [ $1 = "stop" ]; then
    python3 start_stop_instance.py $1
fi

if [ $1 = "run" ]; then
    python3 start_stop_instance.py
fi
