@echo off
set FLASK_APP=server.py
set FLASK_ENV=development
python -m flask run
pause
