from google.oauth2 import service_account
import gspread
import pandas as pd

scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
key = '../credentials/grebi-nu-664c0e090534.json'
credentials = service_account.Credentials.from_service_account_file(key, scopes=scopes)
gc = gspread.authorize(credentials)


def download_sheet(url, sheet):
    """Getting a Google Sheets sheet in pd.DataFrame format

    :param url: link to the file being processed
    :param sheet: name of the sheet to read
    :return: all data in the sheet in pd.DataFrame format
    """

    sh = gc.open_by_url(url)
    data = sh.worksheet(sheet)
    data = pd.DataFrame(data.get_all_records())

    return data


def upload_sheet(url, sheet, data):
    """Save the table in Google Sheets

    :param url: link to the file being processed
    :param sheet: the name of the sheet in which we save the data
    :param data: table to save
    """

    sh = gc.open_by_url(url)
    sh = sh.worksheet(sheet)
    sh.update([data.columns.values.tolist()] + data.values.tolist())

    print('upload sheet completed')
