import gspread
import pandas as pd
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# For information on getting your credentials, see  https://developers.google.com/sheets/api/quickstart/python?hl=pt-br
credentials_path = 'credentials.json'


creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Authorize the gspread client
gc = gspread.authorize(creds)

spreadsheet_id = '1TPMe6wvJkytJ55dky3AtYdBfNbV1ZZkIFBSOr7fzjzY'
worksheet_name = 'Gastos (Python)'

def get_expenses_earnings(spreadsheet, worksheet, exp_last_id=18, earn_first_id=21, earn_last_id=30):
    # Open the Google Spreadsheet by ID and worksheet by name
    worksheet = gc.open_by_key(spreadsheet).worksheet(worksheet)

    # Get all values from the worksheet
    data = worksheet.get_all_values()

    expenses = pd.DataFrame(data[1:exp_last_id], columns=data[0])
    expenses.set_index('Gastos', inplace=True)
    expenses.dropna(how='all', inplace=True)
    expenses.drop(columns='Média', inplace=True)

    earnings = pd.DataFrame(data[earn_first_id:earn_last_id], columns=data[0])
    earnings.set_index(earnings.iloc[:,0], inplace=True)
    earnings.dropna(how='all', inplace=True)
    earnings.drop(columns=['Gastos', 'Média'], inplace=True)
    

    return expenses, earnings





if __name__ == '__main__':
    exp, earn = get_expenses_earnings(spreadsheet_id, worksheet_name)
    
    print(exp.head())
