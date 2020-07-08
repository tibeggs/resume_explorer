from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
includefiles = ['r_config.ini']
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('C:\\Users\\Timothy\\Documents\\GitHub\\resume_explorer\\resume_explorer.py', base=base, targetName = 'resume_app.exe')
]

setup(name='resume_runner',
      version = '0.5',
      description = 'scan resume for keywords',
      options = dict(build_exe = buildOptions),
      executables = executables)
