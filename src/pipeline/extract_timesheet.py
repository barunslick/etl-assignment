""" Extract fact timesheet """

from src.utils.db import execute_sql_from_file
from src.utils import get_path_from_root


def extract_fact_timesheet(conn):
    execute_sql_from_file(conn, get_path_from_root("src/sql/extract_fact_timesheet.sql"), success_msg="Success: [Fact] Added timesheet")