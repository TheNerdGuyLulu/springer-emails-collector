import math
from elsevier import elsevier_emails
from springer import springer_emails


def menu():
    print("Hello there 👋!")

    source = get_and_validate_input('Selection the source\n\t1. Springer (default)\n\t2. Elsevier\n', 1)

    title = input("Insert the title: ")
    subject = input("Insert the subject (optional): ")
    quantity = 50 * math.ceil(get_and_validate_input('Quantity of articles to search: (default 50):', 100) / 50)

    if source == 1:
        springer_emails(title, subject, quantity)
    else:
        elsevier_emails(title, subject, quantity)


def get_and_validate_input(question, default):
    while True:
        try:
            return int(input(question) or default)
        except ValueError:
            print('Invalid number!')
            continue


if __name__ == '__main__':
    menu()
