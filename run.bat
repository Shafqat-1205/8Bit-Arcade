@echo off
REM Activate Conda environment
call "C:\Users\Shafqat\AppData\Local\anaconda3\condabin\activate.bat" amar_jayga

REM Change directory and run the script
cd /d G:\NES
python -u "nes.py"

pause
