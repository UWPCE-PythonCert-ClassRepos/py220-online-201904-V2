#!/usr/bin/env python3

"""
A module that queries the job table and appends those same records
to the Department table.
"""

import logging

from personjob_modeli import *
import sqlite3
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dbCon = sqlite3.connect('personjob.db')

cur = dbCon.cursor()

addColumn = "ALTER TABLE department ADD COLUMN end_date DATE"

cur.execute(addColumn)

dbCon.close()
