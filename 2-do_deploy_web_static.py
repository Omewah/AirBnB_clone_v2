#!/usr/bin/python3
"""a script that distributes an archive to the web servers"""
import os
from fabric.api import env, run, put


env.hosts = ["34.203.77.75", "18.204.8.189"]
"""web server 01 and 02 IP addresses."""


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if os.path.exists(archive_path) is False:
        return(False)
    try:
        put(archive_path, '/tmp/')
        _filename = archive_path.split("/")[-1]
        filename = _filename.split(".")[0]
        run('mkdir -p /data/web_static/releases/{}'.format(filename))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format
            (_filename, filename))
        run('rm /tmp/{}'.format(_filename))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(filename, filename))
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(filename))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'
            .format(filename))
        return(True)
    except:
        return(False)
