"""
The ``pins`` module provides an API for tracking, discovering and sharing datasets.
"""

import os
import yaml
from _pins_cffi import ffi
import subprocess
import platform

def get_rhome():
    r_home = os.environ.get("R_HOME")
    if r_home:
        return r_home
    tmp = subprocess.check_output(("R", "RHOME"), universal_newlines=True)
    r_home = tmp.split(os.linesep)
    if r_home[0].startswith("WARNING"):
        r_home = r_home[1]
    else:
        r_home = r_home[0].strip()
    return r_home

def get_rlib():
    r_home = get_rhome()
    system = platform.system()
    if system == 'Linux':
        lib_path = os.path.join(r_home, 'lib', 'libR.so')
    elif system == 'Darwin':
        lib_path = os.path.join(r_home, 'lib', 'libR.dylib')
    else:
        raise ValueError("System '%s' is unsupported.")
    return lib_path

def open_rlib():
    return ffi.dlopen(get_rlib())

def start():
    os.environ['R_HOME'] = get_rhome()
    rlib = open_rlib()
    status = rlib.Rf_initialize_R(ffi.cast('int', 0), [])

def find_pin():
    """
    Find pins in the active board.
    """
    config_path = os.path.expanduser("~/pins/arrow/config.yml")
    with open(config_path, "r") as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

    return []
