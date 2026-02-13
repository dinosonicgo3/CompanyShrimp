@echo off
title Company Shrimp Service
cd /d %~dp0
echo Starting Company Shrimp Service...
echo [INFO] Flask Web Server starting at http://localhost:18080
cd app
python app.py
pause
