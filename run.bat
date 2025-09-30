@echo off
echo Email Automation System
echo =====================
echo.
echo Choose an option:
echo 1. Setup (First time)
echo 2. Customer Manager
echo 3. Email Automation
echo 4. Create Sample Templates
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Running setup...
    python setup.py
    pause
) else if "%choice%"=="2" (
    echo Starting Customer Manager...
    python customer_manager.py
) else if "%choice%"=="3" (
    echo Starting Email Automation...
    python email_automation.py
) else if "%choice%"=="4" (
    echo Creating sample templates...
    python sample_templates.py
    pause
) else (
    echo Invalid choice!
    pause
)

