from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
import base64
from bs4 import BeautifulSoup
import dateutil.parser as parser

from gm.creds import *
from gm.usr_data import *



# Getting all the unread messages from Inbox
# labelIds can be changed accordingly
unread_msg = GMAIL.users().messages().list(
    userId='me', labelIds=[label_id_1, label_id_2]).execute()

# We get a dictonary. Now reading values for the key 'messages'
mssg_list = unread_msg['messages']

final_list = []

for mssg in mssg_list:
    temp_dict = {}
    m_id = mssg['id']  # get id of individual message
    message = GMAIL.users().messages().get(userId=user_id, id=m_id).execute()  # fetch the message using API
    payld = message['payload']  # get payload of the message
    headr = payld['headers']  # get header of the payload

    for one in headr:  # getting the Subject
        if one['name'] == 'Subject':
            msg_subject = one['value']
            temp_dict['Subject'] = msg_subject

        else:
            pass

    for two in headr:  # getting the date
        if two['name'] == 'Date':
            msg_date = two['value']
            date_parse = (parser.parse(msg_date))
            m_date = (date_parse.date())
            temp_dict['Date'] = str(m_date)
        else:
            pass

    for three in headr:  # getting the Sender
        if three['name'] == 'From':
            msg_from = three['value']
            temp_dict['Sender'] = msg_from
        else:
            pass

    temp_dict['Snippet'] = message['snippet']  # fetching message snippet

    try:

        # Fetching message body
        mssg_parts = payld['parts']  # fetching the message parts
        part_one = mssg_parts[0]  # fetching first element of the part
        part_body = part_one['body']  # fetching body of the message
        part_data = part_body['data']  # fetching data from the body
        clean_one = part_data.replace("-", "+")  # decoding from Base64 to UTF-8
        clean_one = clean_one.replace("_", "/")  # decoding from Base64 to UTF-8
        clean_two = base64.b64decode(bytes(clean_one, 'UTF-8'))  # decoding from Base64 to UTF-8
        soup = BeautifulSoup(clean_two, "lxml")
        mssg_body = soup.body()
        # mssg_body is a readible form of message body
        # depending on the end user's requirements, it can be further cleaned
        # using regex, beautiful soup, or any other method
        temp_dict['Message_body'] = mssg_body

    except:
        pass

    # 	print (temp_dict)
    final_list.append(temp_dict)  # This will create a dictonary item in the final list

# function that takes some message parameters, builds and returns an email message

def build_mesage(destination, obj, body, attachments = []):
    '''Function is called for construct a message'''

    if not attachments:
        message = MIMEText(body)
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
    else:
        message = MIMEMultipart()
        message['to'] = destination
        message['from'] = our_email
        message['subject'] = obj
#         message.attach(MIMEText(body))
#         for filename in attachments:
#             add_attachment(message, filename)
    return {'raw': urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, destination, obj, body, attachments=[]):
    '''Function is called for sending a reply'''
    return service.users().messages().send(
    userId = 'me',
    body=build_mesage(destination,obj,body,attachments)).execute()

