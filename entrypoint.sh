#!/bin/bash
cd /home
git pull
python3 src/lab_questionnaire/manage.py migrate
uwsgi --ini uwsgi.ini
