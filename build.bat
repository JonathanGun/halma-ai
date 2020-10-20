python -m pip install --upgrade buildozer
python -m pip install --upgrade pyinstaller
pyi-makespec --name halma --icon=resource/icon.ico --add-data resource/*;. --add-data *.py;. --onefile main.py
python editspec.py -f=halma.spec
pyinstaller --clean --noconfirm halma.spec
pause