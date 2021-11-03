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

    # dirname = os.path.dirname(project_name)

    # path_dir = path.expanduser()
    path = path.expanduser()
    path_dir = ''
    print(path)
    if (path.is_dir()):
        if (not path.exists()):
            # os.mkdir(path.parents[0])
            os.mkdir(path)
            path_dir = path
            path = str(path.relative_to(path.parent.parent))
        else:
            path_dir = path
    elif (not path.exists()):
        # os.mkdir(path.parents[0])
        os.mkdir(path)
        path_dir = path
        path = str(path.relative_to(path.parent.parent))
    elif (path.exists()):
        path_dir = path
        path = str(path.relative_to(path.parent.parent))
    # elif (os.path.isfile(path)):
    # elif (not path.exists()):
        # os.mkdir(path)
        # path = str(path.relative_to(path.parent.parent))
    else:
        print('Project Name must be a valid name, or directory path')
        return -1
    # setup = path / 'setup.py'
    # setup = path.joinpath('setup.py').name
    # setup = path_dir.joinpath('setup.py').as_posix()
    print(path_dir)
    # setup = str(path_dir)
    setup = str(path_dir / 'setup.py')
    (plumbum.cmd.echo[t.render(
        project_name=project_name,
        alias=alias,
        author=author,
        email=email,
        desc=desc,
        username=username,
        cli=cli)] > setup)()
