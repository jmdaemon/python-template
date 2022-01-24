from wora.file import mkdir
from clopy.tmpl import render, output, promptf, loadcfg, to_path,match
from shutil import copyfile
import datetime
import os

def bang(fp, cmd):
    host            = input('Where will you host [GitHub or GitLab]? [GitHub] : ') or "GitHub"

    hostcfg = {
        'config': {
            'alias': '',
            'username': ''
        }
    }
    gitcfg = {
        'config': {
            'name': '',
            'email': ''
        }
    }

    hostcfg         = loadcfg('github.toml', hostcfg) if host == "GitHub" else loadcfg('gitlab.toml', hostcfg)
    gitcfg          = loadcfg('git.toml', gitcfg)

    project_name    = promptf('What is your new project name? [{}] : ', 'app')
    alias           = promptf('What is your alias? [{}] : ', hostcfg['alias'])
    license         = promptf('Choose a License [MIT or GPLv3]? [{}] : ', 'MIT')
    author          = promptf('What is your full name? [{}] : ', gitcfg['name'])
    username        = promptf('What is your Git username? [{}] : ', hostcfg['username'])
    email           = promptf('What is your Git email? [{}] : ', gitcfg['email'])
    desc            = promptf('Briefly describe your project [{}] : ', '')
    cli             = promptf('Use a CLI library [Click, argparse]? [{}] : ', 'argparse')

    path = to_path(project_name).resolve()
    if (not path.exists()): # If dest doesn't exist
        mkdir(path)
        project_name = path.stem
    elif (len([path.iterdir()]) != 0): # If dest is not empty
        overwrite = ''
        while (not match(overwrite.lower(), ['y', 'n', 'no', 'yes'])):
            overwrite = input((f'{path} is not empty. Overwrite? [y/n]: '))
            if (overwrite.lower() == 'n' or overwrite.lower() == 'no'):
                return 0
        project_name = path.stem

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
        'project_name_caps': project_name.capitalize(),
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
    mkdir(f'{path}/src/{project_name}')
    mkdir(f'{path}/tests')

    # Init git repo
    os.system(f'git init {path}')

    # Output all files
    for name, out in outputs.items():
        output(path, name, out)
    copyfile(f'{fp}/.gitignore', f'{to_path(path)}/.gitignore')
