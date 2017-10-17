import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from apiclient import errors

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Pairing Tool'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'script-python-pairing.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)

        print 'Storing credentials to {}'.format(credential_path)

    return credentials


def execute_script(function, parameters, dev_mode=False):
    SCRIPT_ID = 'MpeAtq155bWlvq9J2GInrUiG4CLBIxOvz'

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('script', 'v1', http=http)

    request = {
        "function": function,
        "parameters": parameters,
        "devMode": dev_mode
        }

    try:
        response = service.scripts().run(body=request,
            scriptId=SCRIPT_ID).execute()

        if 'error' in response:
            error = response['error']['details'][0]
            print 'Script error! Message: {}'.format(error['errorMessage'])
        else:
            return response['response'].get('result', {})
    except errors.HttpError as e:
        print e.content


def get_sheet_as_csv(sheet_name):
    return execute_script('getSheetAsCsv', [sheet_name], True)


def get_sheet(sheet_name):
    return execute_script('getSheet', [sheet_name], True)


if __name__ == '__main__':
    print get_sheet('1')
