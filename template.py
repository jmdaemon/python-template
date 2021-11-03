import plumbum
import os
from pathlib import Path

def mkdir(path, makedir=True):
    if makedir:
        os.mkdir(path)
    return(path, str(path.stem))

def bang(t):
    project_name    = input('New Project Name: ')
    alias           = input('Alias: ')
    author          = input('Full Name of Project Author: ')
    username        = input('Username: ')
    email           = input('Email of Project Author: ')
    desc            = input('Project description: ')
    cli             = input('Use a CLI library? [Click, argparse]: ')

    # Always treat the project name as a directory
    path = Path(project_name)

    path = path.expanduser()
    path_dir = ''
    if (path.is_dir()):
        if (not path.exists()):
            path_dir, project_name = mkdir(path)
        else:
            path_dir, project_name = mkdir(path, makedir=False)
    elif (not path.exists()):
        path_dir, project_name = mkdir(path)
    elif (path.exists()):
        path_dir, project_name = mkdir(path, makedir=False)
    else:
        print('Project Name must be a valid name, or directory path')
        return -1
    print(path_dir)
    print(project_name)
    setup = str(path_dir / 'setup.py')
    (plumbum.cmd.echo[t.render(
        project_name=project_name,
        alias=alias,
        author=author,
        email=email,
        desc=desc,
        username=username,
        cli=cli)] > setup)()
