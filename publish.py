#!/usr/bin/python

import subprocess
from pathlib import Path
import sys
import os
import re

def print_error(error : str, code = -1):
    print("---------------------------- ERROR ----------------------------")
    print("  " + error)
    print("---------------------------------------------------------------")
    exit(code)

def run_command(command, continue_on_fail = False):
    process = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdout, stderr = process.communicate()

    process.wait()

    print(stdout.decode('ascii'))
    print(stderr.decode('ascii'))

    if process.returncode != 0 and not continue_on_fail:
        cmdstr = " ".join([str(c) for c in command])
        print_error(f"The command '{cmdstr}' exited with code {process.returncode}.", process.returncode)



caller_dir = sys.argv[1] if len(sys.argv) > 1 else None

if not os.path.isdir(caller_dir):
    caller_dir = os.path.dirname(caller_dir)

if not os.path.isdir(caller_dir):
    caller_dir = os.getcwd()

version_path = os.path.join(caller_dir, 'version.txt')
version = None

if not os.path.isfile(version_path):
    print_error(f"The file '{version_path}' could not be found.")
else:
    with open(version_path) as f:
        lines = f.readlines()
        version = ''.join(lines).strip()

        if match := re.search('\\d+(\\.\\d+)*', version, re.IGNORECASE):
            version = match.group()

        f.close()

if version is None:
    print_error(f"The file '{version_path}' does not contain an interpretable version.")

try:
    from secrets import nuget_api_key, github_api_key
except:
    print_error("'secrets.py' could not be found.")

print('(re-)building the project ...')
# run_command(['dotnet', 'clean'])
run_command(['dotnet', 'build'])
run_command(['dotnet', 'pack'])

files = [f for f in Path(caller_dir).rglob(f'*.{version}.nupkg')]

print(caller_dir)

if len(files) == 0:
    print_error(f'Found no file to publish matching the version {version} :(')
else:
    print('publishing the following files:\n', files)

for file in files:
    print(f"Publishing '{file}' ...")
    run_command(['dotnet', 'nuget', 'push', file, '-k', nuget_api_key, '-s', 'https://api.nuget.org/v3/index.json'], continue_on_fail = True)
    run_command(['dotnet', 'nuget', 'push', file, '--source', 'github', '--api-key', github_api_key], continue_on_fail = True)

os.system("pause")
