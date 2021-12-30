""" Modules containing gspread client """

from typing import Union, Optional
from gspread.spreadsheet import Spreadsheet
from result import Result, Ok, Err
import gspread
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
CONFIG_FILE = 'staffings-etl-test-335905-0d32bb5fae9a.json'


def get_client(config_file_path: str = CONFIG_FILE,
               scopes: list[str] = SCOPES) -> Result[gspread.client.Client, str]:
    """
    Get gspread client

    :param config_file_path: Path of config file containing keys for GoogleSpecialAccount, defaults to CONFIG_FILE
    :type config_file_path: str, optional
    :param scopes: Scope for authorization, defaults to SCOPES
    :type scopes: list[str], optional
    :return: Gspread client when no error occurs
    :rtype: Result[gspread.client.Client, str]
    """
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            config_file_path, scopes)
        client = gspread.authorize(creds)

        return Ok(client)

    except gspread.exceptions.GSpreadException as error:
        return Err(f"failed to get gspread client:{error}")


def get_spreadsheet_instance(client: gspread.client.Client,
                             spreadsheet_identifier: str,
                             method: Optional[str] = None) -> Result[gspread.spreadsheet.Spreadsheet, str]:
    """
    Get instanace of spreadsheet

    A spreadsheet can be pulled by url, name or id. The method
    parameter can be passed to control this. By default the spreadsheet is searrched by name.

    :param client: Gspread client to access the spreadsheet
    :type client: gspread.client.Client
    :param spreadsheet_identifier: Spreadsheet identifier, maybe name, id or url
    :type spreadsheet_identifier: str
    :param method: By which method to pull spreadsheet By name, url or key
    :type method: Optional[str]
    :return: Spreadheet or Error
    :rtype: Result[gspread.spreadsheet.Spreadsheet, str]
    """
    try:
        spreadsheet = None
        if method == "url":
            spreadsheet = client.open_by_url(spreadsheet_identifier)
        elif method == "key":
            spreadsheet = client.open_by_key(spreadsheet_identifier)
        else:
            spreadsheet = client.open(spreadsheet_identifier)

        return Ok(spreadsheet)
    except gspread.exceptions.SpreadsheetNotFound:
        return Err(f"Error: Couldn't find spreadsheet {spreadsheet_identifier}.")
    except gspread.exceptions.APIError as error:
        return Err(f"Error: API Error -> {error}")


def get_sheet_data(client: gspread.client.Client,
                   spreadsheet_identifier: str,
                   sheet_identifier: Union[str, int],
                   spreadsheet_identifier_type: Optional[str] = None) -> Result[list[dict], str]:
    """
    Get data from a certain sheet.

    A spreadsheet can be pulled by url, name or id. The spreadsheet_identifier_type
    parameter can be passed to control this. By default the spreadsheet is searrched by name.

    :param client: Gspread client
    :type client: gspread.client.Client
    :param spreadsheet_identifier: Spreadsheet unique identifier: name, url or id
    :type spreadsheet_identifier: str
    :param sheet_identifier: Sheet unique identifier
    :type sheet_identifier: Union[str, int]
    :param spreadsheet_identifier_type: By which method to pull spreadsheet By name, url or key
    :type spreadsheet_identifier_type: Optional[str]
    :return: Records from the sheet or Error msg
    :rtype: Result[list[dict], str]
    """
    try:
        spreadsheet = get_spreadsheet_instance(
            client, spreadsheet_identifier, spreadsheet_identifier_type)
        if isinstance(spreadsheet, Err):
            return spreadsheet
        spreadsheet = spreadsheet.value

        sheet_instance = spreadsheet.get_worksheet(sheet_identifier) if isinstance(
            sheet_identifier, int) else spreadsheet.worksheet(sheet_identifier)

        records_data = sheet_instance.get_all_records()

        return Ok(records_data)
    except gspread.exceptions.SpreadsheetNotFound:
        return Err(f"Error: Couldn't find spreadsheet `{spreadsheet_identifier}`.")
    except gspread.exceptions.WorksheetNotFound:
        return Err(f"Error: Couln't find sheet `{sheet_identifier}` inside spreadsheet `{spreadsheet_identifier}`.")
    except gspread.exceptions.APIError as error:
        return Err(f"Error: API Error -> {error}")
