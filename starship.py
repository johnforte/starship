#!/usr/bin/env python3
import yaml
from pathlib import Path
from sh import git
from python_on_whales import docker, DockerClient
import tomllib
import os.path


def read_docker_compose(file):
    with open(file, 'r') as f:
        doc = yaml.load(f, Loader=yaml.FullLoader)
    return doc


configFile = ""

if os.path.isfile("starship.config.toml"):
    configFile = "starship.config.toml"
elif Path.home().joinpath('.starship.config.toml').is_file():
    configFile = Path.home().joinpath('.starship.config.tom')

with open(configFile, "rb") as f:
    config = tomllib.load(f)

repoPath = Path(config['git']['dir_to_clone'])

if not repoPath.joinpath('.git').is_dir():
    git.clone(config['git']['repo'], config['git']['dir_to_clone'])
else:
    git.pull(_cwd=repoPath.absolute())


if config['registery']['private']:
    docker.login(
        config['registery']['url'],
        config['registery']['username'],
        config['registery']['password'],
    )

compose = read_docker_compose(repoPath.joinpath(config['compose']['file']))

if config['compose']['force_repull']:
    for key in compose['services']:
        docker.pull(compose['services'][key]['image'])

docker = DockerClient(compose_files=[repoPath.joinpath(config['compose']['file'])])

docker.compose.up(
    force_recreate=True,
    recreate=True,
)
