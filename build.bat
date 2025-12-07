@echo off
echo ===================================
echo  Compilando Renombrador a .exe
echo ===================================
echo.

REM Instalar dependencias si no estan instaladas
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Compilando con PyInstaller...

python -m PyInstaller --onefile --windowed --clean --noconfirm --name="Renombrador" --icon=NONE renombrador.py

echo.
echo ===================================
echo  Compilacion completa!
echo ===================================
echo.
echo El ejecutable se encuentra en: dist\Renombrador.exe
echo.
pause
