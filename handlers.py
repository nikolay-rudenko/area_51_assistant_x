from helpers import get_alien, print_contacts_table, print_help
from models import Birthday, Email, Phone, Record, AddressBook
from assistant_x import file_name
from functools import wraps
import datetime
import pickle
import os


# Handler decorator
def save_book(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global file_name
        book = kwargs.get("book")
        result = func(*args, **kwargs)
        if not book:
            print("Address cannot be saved. Please try again.")
        else:
            usr_dir = os.path.expanduser("~")
            file_path = os.path.join(usr_dir, file_name)
            with open(file_path, "wb") as file:
                pickle.dump(book, file)
        return result

    return wrapper


# Handle the address book
def get_address_book():
    global file_name
    usr_dir = os.path.expanduser("~")
    file_path = os.path.join(usr_dir, file_name)

    try:
        with open(file_path, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


# Handler functions
@save_book
def add_handler(args, book):
    if len(args) < 3:
        return "Invalid command usage: add <name> <phone>"
    command = ' '.join(args)
    parts = command.split(" ", 2)
    name, phone = parts[1:]

    if len(args) > 3:
        parts = parts[2].split(" ", 2)
        name += ' '+ parts[0]
        phone = parts[1]

    record = Record(name)

    try:
        if not Phone(phone).validate():
            raise ValueError("Invalid phone number")
    except ValueError:
        return "Invalid phone number. Please try again."

    record.add_phone(phone)
    book.add_record(record)
    return f"Contact {name} added"


@save_book
def change_handler(args, book):
    if len(args) != 3:
        return "Invalid command usage: change <name> <new_phone>"
    name, new_phone = args[1:]
    try:
        # Validate the new phone number
        Phone(new_phone)
    except ValueError:
        return "Invalid phone number. Please try again."

    # Attempt to find the contact
    contact = book.find(name)

    # If contact is not found, return an error message
    if not contact:
        return f"Contact {name} not found"

    book.change_phone(name, new_phone)
    return f"Phone number for {name} changed"


def search_handler(args, book):
    if len(args) != 2:
        return "Invalid command usage: find <query>"
    query = args[1]
    contacts = book.find_contacts(query)
    if contacts:
        print_contacts_table(contacts)
        return ''
    else:
        return "No contacts found"


# New handler for changing address
@save_book
def change_address_handler(args, book):
    if len(args) < 3:
        return "Invalid command usage: change_address <name> <new_address>"
    command = ' '.join(args)
    parts = command.split(" ", 2)
    name, new_address = parts[1:]

    # Attempt to find the contact
    contact = book.find(name)

    # If contact is not found, return an error message
    if not contact:
        return f"Contact {name} not found"
    else:
        contact.add_address(new_address)

    return f"Address for {name} changed to {new_address}"


# New handler for changing email
@save_book
def change_email_handler(args, book):
    if len(args) != 3:
        return "Invalid command usage: change_email <name> <new_email>"
    name, new_email = args[1:]

    # Attempt to find the contact
    contact = book.find(name)

    # If contact is not found, return an error message
    if not contact:
        return f"Contact {name} not found"

    book.change_email(name, new_email)
    return f"Email for {name} changed"


# New handler for deleting a record
@save_book
def delete_handler(args, book):
    if len(args) != 2:
        return "Invalid command usage: delete <name>"
    name = args[1]
    if book.find(name):
        book.delete(name)
        return f"Contact {name} deleted"
    else:
        return f"Contact {name} not found"


def all_handler(args, book):
    result = book.show_all()
    if result != "Contacts were not added":
        print_contacts_table(result)
        return ''
    else:
        return result


@save_book
def add_address_hadler(args, book):
    if len(args) < 3:
        return "Invalid command usage: add_address <name> <address>"
    command = ' '.join(args)
    parts = command.split(" ", 2)
    name, address = parts[1:]
    contact = book.find(name)
    if contact:
        contact.add_address(address)
        return f"Address added for {name}"
    else:
        return f"Contact {name} not found"


@save_book
def add_email_handler(args, book):
    if len(args) != 3:
        return "Invalid command usage: add-email <name> <email>"
    name, email = args[1:]
    contact = book.find(name)
    if contact:
        email_obj = Email(email)
        if email_obj.value is None:  # Check if email is invalid
            return "Invalid email address. Please try again."
        else:
            contact.add_email(email)
            return f"Email added for {name}"
    else:
        return f"Contact {name} not found"


@save_book
def add_birthday_handler(args, book):
    if len(args) != 3:
        return "Invalid command usage: add-birthday <name> <birthday>"
    name, birthday = args[1:]
    contact = book.find(name)
    if contact:
        birthday_obj = Birthday(birthday)
        contact.add_birthday(birthday_obj)
        return f"Birthday added for {name}"
    else:
        return f"Contact {name} not found"


def show_birthday_handler(args, book):
    if len(args) != 2:
        return "Invalid command usage: show-birthday <name>"
    name = args[1]
    contact = book.find(name)
    if contact and contact.birthday:
        return f"Birthday for {name}: {contact.birthday}"
    else:
        return f"Contact {name} does not have a birthday or not found"


def show_birthdays_next_week_handler(args, book):
    today = datetime.date.today()
    next_week = today + datetime.timedelta(days=7)
    birthdays = []

    for contact in book.values():
        if contact.birthday:
            birthday_date = datetime.date(contact.birthday.value.year, contact.birthday.value.month,
                                          contact.birthday.value.day,
                                          )
            if (birthday_date.day, birthday_date.month) >= (
                    today.day,
                    today.month,) and (
                    birthday_date.day, birthday_date.month) <= (next_week.day, next_week.month,
                                                                ):
                birthdays.append(contact)
    if birthdays:
        for birthday in birthdays:
            print(f"Upcoming birthdays within the next week:\n {birthday}")
    else:
        "No birthdays within the next week."

    return ""


def show_birthdays_in_period_handler(args, book):
    if len(args) != 2:
        return "Invalid command usage: birthdays-in-period <days>"

    try:
        days = int(args[1])
    except ValueError:
        return "Invalid number of days"

    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=days)

    upcoming_birthdays = []

    for contact in book.values():
        if contact.birthday:
            birthday_month_day = (
                contact.birthday.value.month,
                contact.birthday.value.day,
            )
            today_month_day = (today.month, today.day)
            end_month_day = (end_date.month, end_date.day)

            if today_month_day <= birthday_month_day <= end_month_day:
                upcoming_birthdays.append((contact, contact.days_to_birthday()))

    if upcoming_birthdays:
        result = "Upcoming birthdays in the specified period:\n"
        for contact, days_left in upcoming_birthdays:
            result += f"{contact.name.value}: {days_left} days left\n"
    else:
        result = "No birthdays in the specified period."

    return result


# Added show email handler
def show_email_handler(args, book):
    if len(args) != 2:
        return "Invalid command usage: show_email <name>"
    name = args[1]
    email = book.show_email(name)
    if email:
        return f"Email for {name}: {email}"
    else:
        return f"No email found for {name}"


# Added show address handler
def show_address_handler(args, book):
    if len(args) != 2:
        return "Invalid command usage: show_address <name>"
    name = args[1]
    address = book.show_address(name)
    if address:
        return f"Address for {name}: {address}"
    else:
        return f"No address found for {name}"


# Added delete handler
@save_book
def delete_handler(args, book):
    if len(args) != 2:
        return "Invalid command usage: delete <name>"
    name = args[1]
    if book.find(name):
        book.delete(name)
        return f"Contact {name} deleted"
    else:
        return f"Contact {name} not found"


@save_book
def add_note_handler(args, book):
    if len(args) != 3:
        return "Invalid command usage: add-note <name> <note>"
    name, note = args[1:]
    contact = book.find(name)
    if contact:
        contact.add_note(note)
        return f"Note added for {name}"
    else:
        return f"Contact {name} not found"


@save_book
def edit_note_handler(args, book):
    if len(args) < 4:
        return "Invalid command usage: edit-note <name> <note_index> <new_note>"
    name = args[1]
    note_index = int(args[2])
    new_note = ' '.join(args[3:])
    contact = book.find(name)
    if contact:
        result = contact.edit_note(note_index, new_note)
        if result == "Invalid note index":
            return f"Invalid note index for contact {name}"
        else:
            return f"Note edited for {name}"


def show_note_handler(args, book):
    if len(args) != 2:
        return "Invalid command usage: note <name>"
    name = args[1]
    return book.show_notes(name) or f"Contact {name} not found"


@save_book
def delete_note_handler(args, book):
    if len(args) != 3:
        return "Invalid command usage: delete-note <name> <index>"
    name = args[1]
    note_index = int(args[2])
    contact = book.find(name)
    if contact:
        result = contact.remove_note(note_index)
        if result == "Invalid note index":
            return f"Invalid note index for contact {name}"
        else:
            return f"Note deleted for {name}"
    else:
        return f"Contact {name} not found"


def help_handler(args=None, book=None):
    print_help()
    return ''


def close_handler(args=None, book=None):
    print("Goodbye! 🛸")
    print(get_alien())
    exit(0)
