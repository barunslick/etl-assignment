from src.pipeline.extract_raw_data import extract_raw_employee_data, extract_raw_timesheet_data
from src.pipeline.extract_department import extract_dim_department
from src.pipeline.extract_role import extract_dim_role
from src.pipeline.extract_status import extract_dim_status
from src.pipeline.extract_shift_type import extract_dim_shift_type
from src.pipeline.extract_period import extract_dim_period
from src.pipeline.extract_employee import extract_fact_employee
from src.pipeline.extract_timesheet import extract_fact_timesheet

from src.utils.db import get_database_connection, truncate_table, copy_to_another_table


def truncate_all_tables(conn):
    truncate_table(conn, "raw_timesheet")
    truncate_table(conn, "raw_employee")

    truncate_table(conn, "archive_timesheet")
    truncate_table(conn, "archive_employee")

    truncate_table(conn, "fact_timesheet", cascade=True, reset_identity=True)
    truncate_table(conn, "fact_employee", cascade=True, reset_identity=True)

    truncate_table(conn, "dim_role", cascade=True, reset_identity=True)
    truncate_table(conn, "dim_status", cascade=True, reset_identity=True)
    truncate_table(conn, "dim_department", cascade=True, reset_identity=True)
    truncate_table(conn, "dim_shift", cascade=True, reset_identity=True)
    truncate_table(conn, "dim_period", cascade=True, reset_identity=True)


try:
    conn = get_database_connection("etl-assignment")

    print('-----Starting ETL Process-----')

    print('\n')
    print('-----Truncating all tables----')
    truncate_all_tables(conn)

    print('\n')
    print('-----Extracting raw data into staging tables----')
    extract_raw_employee_data(conn, "./data/employee_2021_08_01.json")
    extract_raw_timesheet_data(
        conn, "./data/timesheet_2021_05_23 - Sheet1.csv")
    extract_raw_timesheet_data(
        conn, "./data/timesheet_2021_06_23 - Sheet1.csv")
    extract_raw_timesheet_data(
        conn, "./data/timesheet_2021_07_24 - Sheet1.csv")

    print('\n')
    print('-----Archiving raw data into archive tables----')
    # Archive  the new extracted data to archive tables
    copy_to_another_table(conn, "raw_employee", "archive_employee")
    copy_to_another_table(conn, "raw_timesheet", "archive_timesheet")

    print('\n')
    print('-----Filling up dimesion tables----')
    extract_dim_role(conn)
    extract_dim_status(conn)
    extract_dim_department(conn)
    extract_dim_shift_type(conn)
    extract_dim_period(conn)

    print('\n')
    print('-----Filling up fact tables----')
    extract_fact_employee(conn)
    extract_fact_timesheet(conn)

    print('\n')
    print('-----ETL Process End----')
finally:
    conn.close()
