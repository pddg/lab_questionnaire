#!/bin/bash
export LC_ALL="en_US.UTF-8"
cd /home
git pull
python3 src/lab_questionnaire/manage.py migrate
chown -R www-data /home
uwsgi --ini uwsgi.ini
