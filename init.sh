#!/bin/bash
service ssh start
python3 app.py &
tail -f /dev/null
