import plumbum
import os
from pathlib import Path

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
    print(path)
    if (path.is_dir()):
        if (not path.exists()):
            os.mkdir(path)
            path_dir = path
            project_name = str(path.stem)
            # project_name = path.name
        else:
            path_dir = path
    elif (not path.exists()):
        os.mkdir(path)
        path_dir = path
        project_name = str(path.stem)
        # project_name = path.name
    elif (path.exists()):
        path_dir = path
        project_name = str(path.stem)
        # project_name = path.name
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
