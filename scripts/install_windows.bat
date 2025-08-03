@echo off
echo Installing AurumCore on Windows 11...
echo.

:: Install Python if not exists
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Installing Python 3.10...
    winget install Python.Python.3.10
    timeout /t 5
)

:: Create virtual environment
python -m venv aurum-env
call aurum-env\Scripts\activate

:: Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install obs-websocket-py transformers numpy flask python-dotenv twitchio sounddevice

:: Setup config
if not exist config mkdir config
copy .env.example .env
echo Please edit the .env file with your credentials

:: Create start script
echo @echo off > start.bat
echo call aurum-env\Scripts\activate >> start.bat
echo python -m aurumcore.core >> start.bat

echo Installation complete!
echo Run 'start.bat' to launch AurumCore
pause
