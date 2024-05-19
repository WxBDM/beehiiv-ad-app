"""Resets all database tables to a default state with default values. This is particularily useful if
we want to start with a clean slate with some dummy variables. This should be run from the command line.
"""
import click

def show_warning(*flags):
    print("=== Warning: you are resetting the database to fill values and variables.")
    print("This will erase all data that is currently there.")
    print(f"You currently have the following flags: {flags}")
    start_script = input("Are you sure this is something you want to do? [y/n]:")
    if start_script.lower() != 'y':
        print("Tables not reset, preserving data.")
        exit()

# @click.group
# @click.pass_context
# def cli(ctx):
#     # Fill this 
#     ctx.obj = {}

# @cli.command(name = 'reset_db')
# @click.option('--fill-dummy', is_flag = True) 
# @click.option('--clean-slate', is_flag = True)
# @click.pass_context
# def reset_db(ctx, fill_dummy, clean_slate):
#     print(fill_dummy, clean_slate)

show_warning()
print("Tables being reverted to default with fill values.")

# Imports
from src import DB as db
from src import app
import src.models as models
import os

# Setup some initial variables
dummy_user_password = os.environ.get('SNAXADS_DEFAULT_DB_PASSWORD', None)
if not dummy_user_password:
    raise ValueError(f'Unable to generate a dummy password. Please ensure the environment is sourced.')

# Connection to the database is in __init__.py.

with app.app_context():

    # Drop and re-create all tables.
    db.drop_all()
    db.create_all()

    # First, set up the `users` table with some fill values.
    sample_users = [
        models.User(firstname='Jane', lastname = 'Doe', username = 'jdoe', email='jane@example.com'),
        models.User(firstname='Paul', lastname = 'M', username = 'pm01892', email='paul@google.com'),
        models.User(firstname='Bill', lastname = 'Gates', username = 'the_bill_gates', email='bill@microsoft.com')
    ]
    for user in sample_users:
        hashed_password = user.password_hash(dummy_user_password)
        db.session.add(user)

    db.session.commit()

# TODO: integrate click

