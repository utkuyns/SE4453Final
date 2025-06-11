#!/bin/bash

/usr/sbin/sshd -p 2222 &

python3 app.py