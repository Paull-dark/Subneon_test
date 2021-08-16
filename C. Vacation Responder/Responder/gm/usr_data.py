from gm.creds import path

user_id = 'me'
# Following email labels can be specified according to
# the user demands.
label_id_1 = 'INBOX'
label_id_2 = 'UNREAD'

# open txt with prepared replies

with open(path + 'body_en.txt', 'r') as file:
    body_en = file.read()

with open(path + 'body_de.txt', 'r') as file:
    body_de = file.read()

with open(path + 'body_ru.txt', 'r') as file:
    body_ru = file.read()





