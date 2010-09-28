#!/usr/bin/env python

import os, subprocess

def find_all_repositories (start_dir=None):
    """ Crawls down from the given path, returning a list of all git repositories found under it"""
    repositories = [] 
    if start_dir == None:
        start_dir = get_repository_root(os.getcwd())

    for root, dirs, files in os.walk(start_dir):
        for dir in dirs:
            if is_git_dir(os.path.join(root, dir)):
                repositories.append(root)

    return repositories

def is_git_dir (dir):
    """ This is taken from the git setup.c:is_git_directory function."""

    if os.path.isdir(dir) and \
            os.path.isdir(os.path.join(dir, 'objects')) and \
            os.path.isdir(os.path.join(dir, 'refs')):
        headref = os.path.join(dir, 'HEAD')
        return os.path.isfile(headref) or \
                (os.path.islink(headref) and
                os.readlink(headref).startswith('refs'))
    return False

def get_repository_root (dir):
    pipe = subprocess.Popen("git rev-parse --show-cdup", shell=True, cwd=dir, 
                            stdout=subprocess.PIPE)
    pipe.wait()
    stdout, stderr = pipe.communicate()

    return os.path.normpath(os.path.join(dir, stdout.rstrip("\n")))

