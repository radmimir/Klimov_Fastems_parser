import PyInstaller.__main__
from os.path import join
import constants

consts = constants.constants()

PyInstaller.__main__.run([
    '--onefile',
    '--noconsole',
    '--icon=%s' % join('.', 'icon.ico'),
    join('', 'forms.py')
])
