import plumbum
import os
from wora.file import read_file
from pathlib import Path
from jinja2 import Template
from shutil import copyfile
import datetime

def mkdir(path, makedir=True):
    if makedir:
        os.mkdir(path)
    return str(path.stem)

def render(src, tmpl_name, vardict):
    tmpl = Template(read_file(str(Path(src) / tmpl_name)))
    res = tmpl.render(vardict)
    return res

def output(dest, tmpl_name, tmpl):
    dest = str(dest / tmpl_name)
    (plumbum.cmd.echo[tmpl] > dest)()

def bang(fp):
    project_name    = input('What is your new project name?         : ')
    alias           = input('What is your alias?                    : ')
    license         = input('Choose a License [MIT, GPLv3]          : ')
    author          = input('What is your full name?                : ')
    username        = input('What is your Git username?             : ')
    email           = input('What is your Git email?                : ')
    desc            = input('Briefly describe your project          : ')
    cli             = input('Use a CLI library? [Click, argparse]   : ')

    path = Path(project_name).resolve()
    if (not path.exists()): # If dest doesn't exist
        project_name = mkdir(path)
    elif (len([path.iterdir()]) != 0): # If dest is not empty
        overwrite = input((f'{path} is not empty. Overwrite? [y/n]: '))
        if (overwrite.lower() == 'n' or overwrite.lower() == 'no'):
            return 0
        project_name = mkdir(path, makedir=False)

    # Ensure the templates render before outputting to dest
    setupdict = {
        'project_name': project_name,
        'license': license,
        'alias': alias,
        'author': author,
        'email': email,
        'desc': desc,
        'username': username,
        'cli': cli
    }
    licensedict = {
        'license': license,
        'year': datetime.date.today().year,
        'author': author
    }
    readmedict = {
        'project_name_caps': project_name.upper(),
        'desc': desc,
        'project_name': project_name,
        'pkgmgr': 'pip',
        'build_sys': '',
        'config_sys': ''
    }

    tmpls = {
        'setup.py': setupdict,
        'LICENSE': licensedict,
        'README.md.tmpl': readmedict,
    }

    # Initialize all templates
    outputs = {}
    for name, vardict in tmpls.items():
        outputs[name.removesuffix(".tmpl")] = (render(fp, name, vardict))

    # Make dest directories
    Path('src').mkdir(parents=True, exist_ok=True)
    Path('tests').mkdir(parents=True, exist_ok=True)

    # Init git repo
    os.system(f'git init {path}')

    # Output all files
    for name, out in outputs.items():
        output(path, name, out)
    copyfile(f'{fp}/.gitignore', f'{Path(path)}/.gitignore')
