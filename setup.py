from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
includefiles = ['r_config.ini']
buildOptions = dict(packages = ['textract'], excludes = [])

base = 'Console'

executables = [
    Executable('C:\\Users\\Timothy\\Documents\\GitHub\\resume_explorer\\resume_explorer.py', base=base, targetName = 'resume_runner.exe')
]

setup(name='resume_runner',
      version = '1',
      description = 'resume keyword scanner',
      options = dict(build_exe = buildOptions),
      executables = executables)
