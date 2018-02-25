#!/bin/sh

exec /usr/bin/uwsgi --ini /application/uwsgi.ini 2>&1
