import imapclient
import pyzmail
from pprint import pprint
from datetime import datetime
from getpass import getpass

username = 'nelouma@yahoo.com'
password = getpass("Email address password ({}): ".format(username))


imapObj = imapclient.IMAPClient('imap.mail.yahoo.com', ssl=True)

imapObj.login(username, password)

imapObj.select_folder('inbox', readonly=True)

email_ids = imapObj.search(['SINCE', '02-Nov-2019', 'FROM', 'senderemail@gmail.com', 'BEFORE', '11-Nov-2019'])

with open('orders.txt', 'w') as f:
    f.write("Serial no.,Date,Order no.,Order title,Page Count,Price\n")

total = 0

for i in range(len(email_ids)):
    raw_messages = imapObj.fetch([email_ids[i]], ['BODY[]', 'INTERNALDATE', 'FLAGS'])

    current_msg = raw_messages[email_ids[i]]
    msg_date = current_msg['INTERNALDATE'.encode('utf-8')] # to get the date the email was sent
    date_sent = datetime.strftime(msg_date, "%d %b %Y") # formating the date

    message = pyzmail.PyzMessage.factory(raw_messages[email_ids[i]][b'BODY[]'])

    subject = message.get_subject()

    pprint(subject)
    pprint(date_sent)
    

    if message.text_part != None:
        #print("++++++++++++++++ Text Email +++++++++++++++++")
        text_body = message.text_part.get_payload().decode(message.text_part.charset)
        #print(text_body)
        pages = text_body.partition("Pages:")[2] #get everything after the word "Pages:"
        head, sep, tail = pages.partition(" pages") # take only the part before  pages/number of words
        print("pages = {}".format(head.lstrip()))
        #print("type of body", type(text_body))
        
    elif message.html_part != None:        
        print("++++++++++++++++ HTML Email +++++++++++++++++")
        html_body = message.html_part.get_payload().decode(message.html_part.charset)
        print(html_body)
        print("type of body", type(html_body))


    with open('orders.txt', 'a') as f:
        order_num = [int(s) for s in subject.split() if s.isdigit()] #extract order number from email subject
        order_title = ''.join(char for char in subject if not char.isdigit()) #clean email subject by removing order number
        pre, separator, suc = order_title.partition("\r")
        if head != "":
            price = int(head)*250
        if len(order_num) != 0 and head != "":
            f.write(str(i) +","+ date_sent +","+ str(order_num[0]) +","+ pre.replace(',','') +","+ head.strip() +","+str(price)+"\n")
            total += price
        else:
            pass

with open('orders.txt', 'a') as f:
    f.write("Total,,,,,{}".format(total))

    
