#!/bin/bash
export LC_ALL="en_US.UTF-8"
python3 /home/src/lab_questionnaire/manage.py migrate
chown -R www-data /home
uwsgi --ini /home/uwsgi.ini
