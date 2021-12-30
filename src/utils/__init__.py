""" General util functions """
import pandas as pd

from src.config import ROOT_DIR

PANDAS_READ_DEFAULTS = {"na_filter": False}

FILE_TYPES_READER = {"xml": pd.read_xml,
                     "csv": pd.read_csv, "json": pd.read_json}


def get_path_from_root(file_path_from_root):
    return f"{ROOT_DIR}/{file_path_from_root}"


def read_data_file(file_path, file_type=None):
    file_type = file_type if file_type is not None else (
        file_path.split("."))[-1]

    file_reader = FILE_TYPES_READER.get(file_type, pd.read_csv)

    data = None
    if file_type == "csv":
        data = file_reader(file_path, **PANDAS_READ_DEFAULTS)
        return data

    return file_reader(file_path)


def create_insert_query(schema: str, csv_db_mapping: dict) -> str:
    values_field = ("%s,"*len(excel_db_mapping))[:-1]
    database_columns = ",".join(list(excel_db_mapping.values()))

    sql_query = f"INSERT INTO {schema}({database_columns}) VALUES ({values_field})"

    return sql_query
