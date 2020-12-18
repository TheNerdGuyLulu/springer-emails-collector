import requests
import concurrent.futures
import math
from bs4 import BeautifulSoup
from datetime import datetime
from functions import write_emails_to_csv


def springer_emails(title: str, subject: str, quantity: int):
    """
    :param title: Article contains title param
    :param subject: Subject of articles to search
    :param quantity: Quantity of articles to search
    """
    emails = set()
    start = datetime.utcnow()

    q = ''
    for keyword in title.split():
        q += f'title:"{keyword}" '

    if subject:
        q += f' subject:"{subject}"'

    # Ceil to multiple of 50
    quantity = 50 * math.ceil(int(quantity) / 50)

    looper = math.ceil(quantity / 50)
    for x in range(0, looper):
        print(str(int(100 * x / looper)) + '%')
        get_articles(q, 50, (x * 50) + 1, emails)

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


def get_articles(q: str, p: int, s: int, emails: set):
    """
    :param q: Query - Article contains title
    :param p: Quantity of results (max 100)
    :param s: Starts at index s
    :param emails: email set to add the emails found
    """
    url = f'http://api.springernature.com/metadata/json?p={p}&s={s}&q={q}&api_key=a710ee53165bdaf3fac89eb940cf2e29'
    try:
        print(url)
        r = requests.get(url)
        r.raise_for_status()
        rjson = r.json()
        session = requests.Session()
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
            futures = []
            for record in rjson['records']:
                for url in record['url']:
                    if url['format'] != 'pdf':
                        futures.append(executor.submit(get_emails, session, url['value'], emails))
                        break
            for future in concurrent.futures.as_completed(futures):
                pass  # write to file here
    except requests.exceptions.HTTPError as e:
        print(f'Request failed - {url}')


def get_emails(session: requests.Session, url: str, emails: set):
    """
    :param session: Session instance to keep connection open, fastening the process
    :param url: URl of a single article
    :param emails: email set to add the emails found
    """
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    for author in soup.find_all('meta', {'name': 'citation_author_email'}):
        emails.add(author.attrs['content'])
