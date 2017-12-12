#!/bin/bash
cd /home
git pull
uwsgi --ini uwsgi.ini
