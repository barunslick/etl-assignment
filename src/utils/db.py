""" Methods to connect to database """
import psycopg2
import psycopg2.extras as extras

from src.config import DB_HOST, DB_PORT, DB_USERNAME, DB_PASSWORD


def get_database_connection(schema_name: str,
                            host=DB_HOST,
                            port=DB_PORT,
                            user=DB_USERNAME,
                            password=DB_PASSWORD,
                            ):

    return psycopg2.connect(host=host,
                            port=port,
                            user=user,
                            password=password,
                            database=schema_name)


def execute_sql(conn, sql, success_msg="Query executed successfully"):
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql)
            print(success_msg)

def execute_sql_from_file(conn, filepath, success_msg="Query executed successfully"):
    with open(filepath, 'r') as file:
        sql = file.read()
        execute_sql(conn, sql, success_msg)


def truncate_table(conn, table_name, cascade=False, reset_identity=False):
    sql = f"TRUNCATE TABLE  {table_name}"

    if reset_identity:
        sql = f"{sql} RESTART IDENTITY"

    if cascade:
        sql = f"{sql} CASCADE"

    with conn:
        with conn.cursor() as curs:
            curs.execute(sql)
            print(f"Success: Truncated {table_name}")


def copy_to_another_table(conn, source_table_name, destination_table_name):
    sql = f"INSERT INTO {destination_table_name} SELECT * FROM {source_table_name}"
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql)
            print(
                f"Copied from {source_table_name} to {destination_table_name}")


def execute_values(conn, df, table_name, success_msg="Successful insertion of data"):
    """
    Using psycopg2.extras.execute_values() to insert the dataframe
    """

    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))

    # SQL quert to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table_name, cols)

    with conn:
        with conn.cursor() as curs:
            extras.execute_values(curs, query, tuples)
            print(success_msg)
