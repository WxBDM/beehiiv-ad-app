"""Contains initialization steps of the application. These are, as follows:

- Loading the .env file and ensuring that it's sourced,
- Initalizing the application with the Flask object
- Connecting to the database
- Setting up logging

Note: the path should be pointing to the base repository.
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from dotenv import load_dotenv
import logging
import pymysql
import sys

class EnvVariableError(Exception):
    """An error specific to env file/variables.
    
    This may be removed and not necessary."""
    pass

#########################
# Environment Variables #
#########################
load_dotenv()

logging.info(f'__init__ file being invoked.')
logging.info(f'Loaded environment file. Sample: {os.environ.get("SNAXADS_SAMPLE_ENV_VARIABLE", None)}')

############
# App Init #
############
template_folder = os.environ.get('SNAXADS_TEMPLATE_LOCATION', None)
if not template_folder:
    raise EnvVariableError(f'Template location not found. Is the env file sourced?')

APP = Flask(__name__, template_folder=template_folder)

#################
# Database Init #
#################
db_name = os.environ.get('SNAXADS_SQL_DATABASE', None)
if not db_name:
    raise ValueError(f'DB Name not found. Is the env file sourced?')

pymysql.install_as_MySQLdb()
APP.config['SQLALCHEMY_DATABASE_URI'] = db_name
DB = SQLAlchemy(APP)