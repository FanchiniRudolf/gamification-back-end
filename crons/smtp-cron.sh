#!/bin/bash
export PYTHONPATH=$PYTHONPATH:"/home/ubuntu/gamificacion"
cd /home/ubuntu/gamificacion/crons
python3 SmtpClientCrontab.py >> /home/ubuntu/logs/smtp.log 2>&1