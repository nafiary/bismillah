from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64

SCOPES = 'https://mail.google.com/'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
    try:
        send = service.users().messages().send(userId=user_id, body=message).execute()
        print ('Message Id: %s' % send['id'])
        return send
    except Exception as error:
        print ('An error occurred: %s' % error)

message = create_message('kebobunting2@gmail.com', 'afifridhokamalputra@gmail.com', 'testapi', 'testtest')
# print (message)
send_message(service, 'me', message)

# Call the Gmail API
# results = service.users().labels().list(userId='me').execute()
# labels = results.get('labels', [])
# # print (results)
# if not labels:
#     print('No labels found.')
# else:
#     print('Labels:')
#     for label in labels:
#         print(label['name'])
# [END gmail_quickstart]
