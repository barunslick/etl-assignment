""" Extract status dimensions"""

from src.utils.db import execute_sql_from_file
from src.utils import get_path_from_root


def extract_dim_status(conn):
    execute_sql_from_file(conn, get_path_from_root("src/sql/extract_status_from_raw.sql"), success_msg="Success: [Dimension] Added status")