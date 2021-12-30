""" Contains global app configuration and settings """
import os

# ROOT PROJECT DIR
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# DATABASE CONNECTION CONFIG
DB_HOST = "localhost"
DB_USERNAME = "postgres"
DB_PASSWORD = None
DB_PORT = 5432
