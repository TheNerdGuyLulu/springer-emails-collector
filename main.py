import requests
import math
import concurrent.futures
from bs4 import BeautifulSoup
import csv
from datetime import datetime


def menu():
    print("Hello there 👋!")
    title = input("Insert the title: ")
    subject = input("Insert the subject (optional): ")
    while True:
        quantity = input('Quantity of articles to search: (default 100):') or 100
        try:
            quantity = 100 * math.ceil(int(quantity) / 100)
        except ValueError:
            print('Invalid number!')
            continue
        else:
            break

    springer_emails(title, subject, quantity)


def springer_emails(title, subject, quantity):
    """
    :param title: Article contains title param
    :param subject: Subject of articles to search
    :param quantity: Quantity of articles to search
    """
    emails = set()
    start = datetime.utcnow()

    q = f'title:"{title}"'
    if subject:
        q += f' subject:"{subject}"'

    rangeup = math.ceil(quantity / 100)
    for x in range(0, rangeup):
        print(str(int(100 * x / rangeup)) + '%')
        get_articles(q, 100, (x * 100) + 1, emails)

    if len(emails) == 0:
        print("No email found!")
    else:
        for email in emails:
            print(email)
        elapsed = datetime.utcnow() - start
        print(elapsed)
        print_to_file = input("Write to csv file? [Y/n]") or 'Y'
        print(print_to_file)
        if print_to_file.upper() == 'Y':
            write_emails_to_csv(emails)


def get_articles(q, p, s, emails):
    """
    :param q: Query - Article contains title
    :param p: Quantity of results (max 100)
    :param s: Starts at index s
    :param emails: email set to add the emails found
    """
    try:
        r = requests.get(f'http://api.springernature.com/metadata/json?p={p}&s={s}&q={q}&api_key=a710ee53165bdaf3fac89eb940cf2e29')
        r.raise_for_status()
        rjson = r.json()
        session = requests.Session()
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            for record in rjson['records']:
                for url in record['url']:
                    if url['format'] != 'pdf':
                        futures.append(executor.submit(get_emails, session, url['value'], emails))
                        break;
            for future in concurrent.futures.as_completed(futures):
                pass  # write to file here
    except requests.exceptions.HTTPError as e:
        print(f'Request failed - http://api.springernature.com/metadata/json?p={p}&s={s}&q={q}&api_key=a710ee53165bdaf3fac89eb940cf2e29')


def get_emails(session, url, emails):
    """
    :param session: Session instance to keep connection open, fastening the process
    :param url: URl of a single article
    :param emails: email set to add the emails found
    """
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for author in soup.find_all('meta', {'name': 'citation_author_email'}):
        emails.add(author.attrs['content'])


def write_emails_to_csv(emails):
    """
    :param emails: email set to write to file
    """
    with open('emails-' + str(datetime.utcnow()) + '.csv', mode='w') as emails_file:
        emails_writer = csv.writer(emails_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for email in emails:
            emails_writer.writerow([email])


if __name__ == '__main__':
    menu()
