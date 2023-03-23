import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleSheet:
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    def __init__(self, spreadsheet_id):
        self.spreadsheet_id = spreadsheet_id
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                print('flow')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    def getRangeValues(self, range):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range).execute()
        return result

    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
    
    def appendRangeValues(self, range, values):
        body = {
            'range': range,
            'majorDimension': 'ROWS',
            'values': values,
            }
        result = self.service.spreadsheets().values().append(spreadsheetId=self.spreadsheet_id, range=range, body=body, valueInputOption='USER_ENTERED').execute()


async def create_profile_gs(gs, user_id):
    users = gs.getRangeValues('Лист1!A1:A')
    try:
        users = [int(value[0]) for value in users.get('values')]
    except:
        users = []

    if not user_id in users: 
        gs.appendRangeValues('Лист1!A1', [[user_id]])


async def edit_profile_gs(gs, state, user_id):
    users = gs.getRangeValues('Лист1!A1:A')
    try:
        users = [int(value[0]) for value in users.get('values')]
    except:
        return

    try:
        range_id = users.index(user_id) + 1
    except:
        return
    
    async with state.proxy() as data:
        values = [
            [data['name'], data['phone']]
        ]
        range_edit = f'Лист1!B{range_id}:C{range_id}'
        gs.updateRangeValues(range_edit, values) 

def main():
    gs = GoogleSheet(spreadsheet_id='1asgcW-3DSjn8SJFxLkRsuyNZ63SPkNJblAnkZK8ogcU')
    # print(gs.getRangeValues('Лист1!A1:A'))
    create_profile_gs(gs, 11)

if __name__ == '__main__':
    main()