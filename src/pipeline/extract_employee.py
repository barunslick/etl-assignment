""" Extract facts from raw and dimension tables"""

from src.utils.db import execute_sql_from_file
from src.utils import get_path_from_root


def extract_fact_employee(conn):
    execute_sql_from_file(conn, get_path_from_root("src/sql/extract_fact_employee.sql"), success_msg="Success: [Fact] Added employee")
