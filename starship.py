#!/usr/bin/env python3
import yaml
from pathlib import Path
from sh import git
from python_on_whales import docker, DockerClient
import toml
import os.path


def read_docker_compose(file):
    with open(file, 'r') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
    return doc


def find_toml_config():
    if os.path.isfile("starship.config.toml"):
        return "starship.config.toml"
    elif Path.home().joinpath('.starship.config.toml').is_file():
        return Path.home().joinpath('.starship.config.tom')


config_file = find_toml_config()

config = toml.load(config_file)

repo_path = Path(config['git']['dir_to_clone'])

if not repo_path.joinpath('.git').is_dir():
    git.clone(config['git']['repo'], config['git']['dir_to_clone'])
else:
    git.pull(_cwd=repo_path.absolute())


docker = DockerClient(
    compose_files=[repo_path.joinpath(config['compose']['file'])]
)

if config['registry']['private']:
    docker.login(
        config['registry']['url'],
        config['registry']['username'],
        config['registry']['password'],
    )

compose = read_docker_compose(repo_path.joinpath(config['compose']['file']))

if config['compose']['force_repull']:
    for key in compose['services']:
        docker.pull(compose['services'][key]['image'])

docker.compose.up(
    remove_orphans=True,
    detach=True,
    force_recreate=True,
    recreate=True,
)
