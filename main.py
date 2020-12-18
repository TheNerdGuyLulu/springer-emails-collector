from functions import validate_input_as_int
from springer import springer_emails


def menu():
    print("Hello there 👋!")
    source = validate_input_as_int('Source:\n\t1. Springer (default)\n\t2. Elsevier\n', 1)
    title = input("Insert the title: ")
    subject = input("Insert the subject (optional): ")
    quantity = validate_input_as_int('Quantity of articles to search: (default 50):', 50)

    if source == 1:
        springer_emails(title, subject, quantity)
    else:
        print("To be implemented")


if __name__ == '__main__':
    menu()
