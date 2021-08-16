# Importing required libraries
import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# Request all access (permission to read/send/receive emails, manage the inbox, and more)
SCOPES = ['https://mail.google.com/'] # Gmail address
our_email = 'User_user@gmail.com' # User's e-mail
path = 'C:/Users/username/Gmail/Responder/gm/' # User's path to folder

def gmail_authentificate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists(path + 'token.pickle'):
        with open(path + 'token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials avaliable, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(path + 'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for next run
        with open (path + 'token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

# get the gmail API service
GMAIL = gmail_authentificate()