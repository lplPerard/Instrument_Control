# -*- coding: utf-8 -*-

# A simple setup script to create an executable using Tkinter.

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

includefiles = ['Release_note.txt', 'README.txt', 'NIVISA_19.5.exe']

executables = [
    Executable('CBRAM_Software.py', base=base, icon='icon.ico')
]

setup(name='CBRAM testbench',
      version='1.0',
      author='LPStudio',
      options = {'build_exe': {'include_files':includefiles}},    
      executables=executables
      )