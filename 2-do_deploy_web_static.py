#!/usr/bin/python3
"""a script that distributes an archive to the web servers"""
import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ["34.203.77.75", "18.204.8.189"]
"""web server 01 and 02 IP addresses."""


@runs_once
def do_pack():
    """archive the contents of the web_static folder"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    current_time = datetime.now()
    output = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        current_time.year,
        current_time.month,
        current_time.day,
        current_time.hour,
        current_time.minute,
        current_time.second
    )
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output


def do_deploy(archive_path):
    """Distributes an archive to the web servers"""
    if not os.path.exists(archive_path):
        return False
    filename = os.path.basename(archive_path)
    foldername = filename.replace(".tgz", "")
    pathfolder = "/data/web_static/releases/{}/".format(foldername)
    success = False
    try:
        put(archive_path, "/tmp/{}".format(filename))
        run("mkdir -p {}".format(pathfolder))
        run("tar -xzf /tmp/{} -C {}".format(filename, pathfolder))
        run("rm -rf /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(pathfolder, pathfolder))
        run("rm -rf {}web_static".format(pathfolder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(pathfolder))
        print('New version deployed!')
        success = True
    except Exception:
        success = False
    return success
