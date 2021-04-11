import imaplib
import email
from typing import List, Optional
from dateutil.parser import parse
from decouple import config
from remind_me_api.sms import PASSWORD

EMAIL: str = config('EMAIL')
PASSWORD: str = config('PASSWORD')


class ReadEmail:
    def __init__(self, email: str = EMAIL, password: str = PASSWORD):
        self.email = email
        self.password = password
        self.imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        self.messages = []


    def __enter__(self):
        self.imap.login(self.email, self.password)
        self.imap.select('"[Gmail]/All Mail"')
        return self
    

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.imap.close()
        self.imap.logout()


    def get_messages(self) -> Optional[List[List]]:
        result, data = self.imap.uid('search', None, '(UNSEEN)')
        if result == 'OK':
            for num in data[0].split():
                temp = []
                result, data = self.imap.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    email_message = email.message_from_bytes(data[0][1])
                    temp.append(email_message['From'])
                    if email_message.is_multipart():
                        for part in email_message.get_payload():
                            temp.append(part.get_payload())
                    else:
                        temp.append(email_message.get_payload())
                self.messages.append(temp)
                    
        return self.messages or None


def main() -> Optional[List[tuple]]:
    jobs: List = []
    chars: str = '0123456789:-'

    with ReadEmail() as reader:
        messages = reader.get_messages()
        if messages is not None:
            for message in messages:
                number, carrier = message[0].split('@')
                date_and_time = parse(message[1], fuzzy=True)
                msg = ''.join([m for m in message[1] if m not in chars]).strip()
                package = (number, carrier, msg, date_and_time)
                jobs.append(package)
    
    return jobs or None


if __name__ == '__main__':
    print(main())
