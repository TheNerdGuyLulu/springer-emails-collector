import csv
from datetime import datetime


def write_emails_to_csv(emails):
    """
    :param emails: email set to write to file
    """
    with open('emails-' + str(datetime.utcnow()) + '.csv', mode='w') as emails_file:
        emails_writer = csv.writer(emails_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for email in emails:
            emails_writer.writerow([email])
