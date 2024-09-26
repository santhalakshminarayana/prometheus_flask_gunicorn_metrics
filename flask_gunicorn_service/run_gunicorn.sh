#!/bin/bash
cd /app
exec gunicorn 'main:run()'
