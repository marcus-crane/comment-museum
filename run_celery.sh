#!/bin/sh

# Wait for rabbitmq to spin up
sleep 10

cd comments

su -c "celery worker -A museum --beat --loglevel=info"