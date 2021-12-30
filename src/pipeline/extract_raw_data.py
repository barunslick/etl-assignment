""" Extract staffing data """

from src.utils import read_data_file
from src.utils.db import execute_values


def extract_raw_employee_data(con, file_path):

    employee_df = read_data_file(file_path)

    execute_values(con, employee_df, "raw_employee", success_msg="Success: [Raw] Extracted raw employee")


def extract_raw_timesheet_data(con, file_path):
    timesheet_df = read_data_file(file_path)

    execute_values(con, timesheet_df, "raw_timesheet", success_msg="Success: [Raw] Extracted raw timesheet")
