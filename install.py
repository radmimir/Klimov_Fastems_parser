import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    '--onefile',
    os.path.join('', 'parser.py'),
])