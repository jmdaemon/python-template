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

    # Ensure the templates render before outputting to dest
    # Init setup.py template
    setup = str(path / 'setup.py')
    t = Template(read_file(f'{fp}/setup.py'))
    setup_out = plumbum.cmd.echo[t.render(
        project_name=project_name,
        license=license,
        alias=alias,
        author=author,
        email=email,
        desc=desc,
        username=username,
        cli=cli)]

    # Init License template
    lt = Template(read_file(str(Path(fp) / 'LICENSE')))
    lout = str(path / 'LICENSE')
    year = datetime.date.today().year
    license_out = plumbum.cmd.echo[lt.render(
        license=license,
        year=year,
        author=author
    )]

    # Init README.md template
    rt = Template(read_file(str(Path(fp) / 'README.md.tmpl')))
    readme = str(path / 'README.md')
    readme_out = plumbum.cmd.echo[rt.render(
        project_name_caps=project_name.upper(),
        desc=desc,
        project_name=project_name,
        pkgmgr='pip',
        build_sys='',
        config_sys=''
    )]

    # Make directories
    Path('src').mkdir(parents=True, exist_ok=True)
    Path('tests').mkdir(parents=True, exist_ok=True)

    # Create git repository
    os.system(f'git init {path}')

    # Output all files
    (setup_out > setup)()
    (license_out > lout)()
    (readme_out > readme)()
