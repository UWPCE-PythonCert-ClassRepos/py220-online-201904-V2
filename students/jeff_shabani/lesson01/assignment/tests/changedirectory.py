#!/usr/bin/env python3

"""Module to change the working directory to
 inventory_management for testing
 """

import os
from pathlib import Path

def changedirectory():
    current_path = str(Path.cwd())
    new_path = current_path.replace('tests','inventory_management')
    os.chdir(new_path)
