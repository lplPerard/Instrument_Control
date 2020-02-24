# -*- coding: utf-8 -*-

# A simple setup script to create an executable using Tkinter.

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('CBRAM_Software.py', base=base, icon='icon.ico')
]

setup(name='CBRAM testbench',
      version='1.0',
      description='Testbench to evaluate CBRAM cells for RF switche applications',
      executables=executables
      )