import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from decouple import config

EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')

# carriers = {
#     'att': 'mms.att.net',
#     'tmobile': 'tmomail.net',
#     'verizon': 'vtext.com',
#     'sprint': 'pm.sprint.com'
# }

suffixes = {'com', 'net'}

class InvalidCarrier(Exception):
    pass


def send(message, number, carrier):
    # if carrier.lower() not in carriers:
    #     if carrier.split('.')[1] not in suffixes:
    #         raise InvalidCarrier(f"'{carrier}' is not a valid carrier.")
    
    # carrier = carriers[carrier].lower() or carrier
    to_number = str(number)+'@{}'.format(carrier)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(EMAIL, PASSWORD)

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_number
    msg.attach(MIMEText(message, 'plain'))
    sms = msg.as_string()


    server.sendmail(EMAIL, to_number, sms)
    msg = ''
    server.quit()