"""Contains initialization steps of the application. These are, as follows:

- Loading the .env file and ensuring that it's sourced,
- Initalizing the application with the Flask object
- Connecting to the database
- Setting up logging
"""

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from dotenv import load_env

class EnvVariableError(Exception):
    """An error specific to env file/variables.
    
    This may be removed and not necessary."""
    pass

#########################
# Environment Variables #
#########################
load_env()

# Check the templates folder and initalize the app.
template_folder = os.environ.get('SNAXADS_TEMPLATE_LOCATION', None)
if not template_folder:
    raise EnvVariableError(f'Template location not found. Is the env file sourced?')

############
# App Init #
############
app = Flask(__name__, template_folder=template_folder)

#################
# Database Init #
#################
db_name = os.environ.get('SNAXADS_SQL_DATABASE', None)
if not db_name:
    raise ValueError(f'DB Name not found. Is the env file sourced?')

app.config['SQLALCHEMY_DATABASE_URI'] = db_name
DB = SQLAlchemy(app)
DB.init_app(app)

# whatever else goes down here...