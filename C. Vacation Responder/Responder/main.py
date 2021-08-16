import time
from textblob import TextBlob

from gm.usr_data import *
from gm.creds import *
from gm.checker import *

if __name__ == '__main__':
    print("** Hola! I'm Autoresponder! Model T-800\n")

    # Run for execution
    for i in final_list:
        # TextBolb is checking the language
        lang = TextBlob(i['Snippet']).detect_language()
        if lang == 'de':
            send_message(GMAIL, i['Sender'], 'AutoReply', body_de)
        elif lang == 'ru':
            send_message(GMAIL, i['Sender'], 'AutoReply', body_ru)
        else:
            send_message(GMAIL, i['Sender'], 'AutoReply', body_en)
        time.sleep(2)

    # This will mark the message as read
    GMAIL.users().messages().modify(userId=user_id,
                                    id=m_id,
                                    body={
                                        'removeLabelIds': ['UNREAD']
                                    }).execute()