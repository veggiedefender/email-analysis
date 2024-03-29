"""Downloads all emails to a compressed pickle named emails.pickle.gz
RAM usage varies based on the number of emails associated with the account,
but I recorded 3.5 GB of usage.
"""
import imaplib
import email
import getpass
import gzip
import pickle

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(input("Email: "), getpass.getpass("Password: "))
mail.select("inbox")

result, data = mail.search(None, "ALL")
ids_list = data[0].split()

emails = []
i = 0

def parse_bytes(data):
    """
    Parses email data into a string readable by email.message_from_string.
    Tries decoding utf-8, or cp1252 (Windows format) if that fails.
    """
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252")

for email_id in ids_list:
    status, data = mail.fetch(email_id, "(RFC822)")
    if status != "OK":
        print(f"Failed to fetch message {email_id}")
        continue
    try:
        raw_message = parse_bytes(data[0][1])
        message = email.message_from_string(raw_message)
        emails.append(message)
        print(f"Downloaded {int(email_id)}/{len(ids_list)}\r", end="")
    except Exception as e:
        print(e)
        print(f"Failed to parse message {email_id}")

file = gzip.open("emails.pickle.gz", "wb+")
pickle.dump(emails, file)
