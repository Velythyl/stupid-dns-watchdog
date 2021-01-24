import contextlib
import os
import subprocess


@contextlib.contextmanager
def makedirs(name):
    try:
        os.makedirs(name)
    except:
        pass
    yield None

@contextlib.contextmanager
def directory(name):
    ret = os.getcwd()
    os.chdir(name)
    yield None
    os.chdir(ret)
