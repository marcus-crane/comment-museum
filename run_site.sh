#!/bin/sh

# Wait for postgres to spin up
sleep 10

cd comments

su -c "python manage.py makemigrations"
su -c "python manage.py migrate archival"