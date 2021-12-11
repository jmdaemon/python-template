import plumbum
import os
from wora.file import read_file
from pathlib import Path
from jinja2 import Template
import datetime

def mkdir(path, makedir=True):
    if makedir:
        os.mkdir(path)
    return str(path.stem)

def bang(fp):
    project_name    = input('New Project Name: ')
    alias           = input('Alias: ')
    license         = input('Project License [MIT, GPLv3]: ')
    author          = input('Full Name of Project Author: ')
    username        = input('Username: ')
    email           = input('Email of Project Author: ')
    desc            = input('Project description: ')
    cli             = input('Use a CLI library? [Click, argparse]: ')

    path = Path(project_name).expanduser()

    if (path.is_dir()):
        if (not path.exists()):
            project_name = mkdir(path)
        else:
            project_name = mkdir(path, makedir=False)
    elif (not path.exists()):
        project_name = mkdir(path)
    elif (path.exists()):
        project_name = mkdir(path, makedir=False)
    else:
        print('Project Name must be a valid name, or directory path')
        return -1

    # Create git repository
    os.system(f'git init {path}')

    # Create README.md
    readme = path / 'README.md'
    os.system(f'touch {readme}')

    # Make directories
    Path('src').mkdir(parents=True, exist_ok=True)
    Path('tests').mkdir(parents=True, exist_ok=True)

    # Create initial setup.py
    setup = str(path / 'setup.py')
    t = Template(read_file(f'{fp}/setup.py'))

    (plumbum.cmd.echo[t.render(
        project_name=project_name,
        license=license,
        alias=alias,
        author=author,
        email=email,
        desc=desc,
        username=username,
        cli=cli)] > setup)()

    # Create License
    lt = Template(read_file(str(Path(fp) / 'LICENSE')))
    lout = str(path / 'LICENSE')
    year = datetime.date.today().year

    (plumbum.cmd.echo[lt.render(
        license=license,
        year=year,
        author=author
    )] > lout)()
