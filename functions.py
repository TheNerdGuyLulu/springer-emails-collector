import csv
from datetime import datetime


def validate_input_as_int(message: str, default: int):
    while True:
        try:
            return int(input(message) or default)
        except ValueError:
            print('Invalid number!')
            continue


def write_emails_to_csv(emails: set):
    """
    :param emails: email set to write to file
    """
    with open('emails-' + str(datetime.utcnow()) + '.csv', mode='w') as emails_file:
        emails_writer = csv.writer(emails_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for email in emails:
            emails_writer.writerow([email])
