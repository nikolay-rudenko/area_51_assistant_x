from helpers import print_app_intro, print_help, print_contacts_table, get_alien
from collections import UserDict
import datetime
import os
import pickle
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Note(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            raise ValueError("Invalid phone number")

    def validate(self):
        return len(self.value) == 10 and self.value.isdigit()


class Address(Field):
    pass


class Email(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            self.value = None

    def validate(self):
        pattern = r'^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$'
        return re.match(pattern, self.value) is not None


class Birthday(Field):
    def __init__(self, date_string):
        self.value = self.validate(date_string)
        if not self.value:
            raise ValueError("Invalid birthday format. Use DD.MM.YYYY")

    def validate(self, date_string):
        try:
            return datetime.datetime.strptime(date_string, "%d.%m.%Y")
        except ValueError:
            return None


class Record:
    """
    Цей клас описує запис у адресній книзі.

    Атрибути:
        name (str): Ім'я контакту.
        phones (list): Список номерів телефонів контакту.
        birthday (datetime.date): Дата народження контакту.
        address (str): Адреса контакту.
        email (str): Адреса електронної пошти контакту.
        notes (list): Список нотаток про контакт.

    Методи:
        add_phone(phone_number: str): Додати номер телефону до списку телефонів.
        remove_phone(phone_number: str): Видалити номер телефону зі списку телефонів.
        edit_phone(old_number: str, new_number: str): Змінити номер телефону в списку.
        find_phone(phone_number: str): Знайти номер телефону в списку.
        add_birthday(birthday: datetime.date): Додати дату народження.
        days_to_birthday(): Розрахувати дні до дня народження.
        show_notes(): Показати всі нотатки.
        add_note(note: str): Додати нотатку.
        edit_note(note_index: int, new_note: str): Змінити нотатку.
        remove_note(note_index: int): Видалити нотатку.
    """

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.address = None
        self.email = None
        self.notes = []

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def add_address(self, address):
        self.address = Address(address)

    def add_email(self, email):
        email_obj = Email(email)
        if email_obj.value is None:  # Check if email is invalid
            print("Invalid email address. Please try again.")
        else:
            self.email = email_obj

    def add_note(self, note):
        self.notes.append(Note(note))

    def remove_phone(self, phone_number):
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break

    def find_phone(self, phone_number):
        return next(
            (phone for phone in self.phones if phone.value == phone_number), None
        )

    def edit_note(self, note_index, new_note):
        if note_index < 0 or note_index >= len(self.notes):
            return "Invalid note index"
        self.notes[note_index] = Note(new_note)

    def remove_note(self, note_index):
        if note_index < 0 or note_index >= len(self.notes):
            return "Invalid note index"
        del self.notes[note_index]

    def show_notes(self):
        return '; '.join(note.value for note in self.notes)

    def add_birthday(self, birthday):
        self.birthday = birthday
        return True

    def days_to_birthday(self):
        if not self.birthday:
            return None

        today = datetime.date.today()
        birthday_date = datetime.date(
            today.year, self.birthday.value.month, self.birthday.value.day
        )

        if (
            birthday_date < today
        ):  # If birthday has passed this year, calculate for next year
            birthday_date = datetime.date(
                today.year + 1, self.birthday.value.month, self.birthday.value.day
            )

        return (birthday_date - today).days

    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if hasattr(self, 'birthday') and self.birthday:
            result += f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        else:
            result += ", No birthday"
        if hasattr(self, 'address') and self.address:
            result += f", address: {self.address.value}"
        else:
            result += ", No address"
        if hasattr(self, 'email') and self.email:
            result += f", email: {self.email.value}"
        else:
            result += ", No email"
        return result



class AddressBook(UserDict):
    """
        Цей клас описує адресну книгу.

        Атрибути:
            data (dict): Словник, де ключем є ім'я контакту, а значенням - екземпляр класу Record.

        Методи:
            add_record(record: Record): Додати запис до адресної книги.
            find(name: str): Знайти запис за ім'ям.
            delete(name: str): Видалити запис за ім'ям.
            change_phone(name: str, new_phone: str): Змінити номер телефону для контакту.
            show_phone(name: str): Показати номер телефону для контакту.
            show_notes(name: str): Показати всі нотатки для контакту.
            show_all(): Показати всі записи в адресній книзі.
        """

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def change_phone(self, name, new_phone):
        record = self.data.get(name)
        if record and record.phones:
            old_phone = record.phones[0].value
            record.edit_phone(old_phone, new_phone)

    # New method to change email
    def change_email(self, name, new_email):
        record = self.data.get(name)
        if record:
            record.add_email(new_email)

    # New method to change address
    def change_address(self, new_address):
        self.address = new_address


    def show_phone(self, name):
        record = self.data.get(name)
        if record:
            return "; ".join(phone.value for phone in record.phones)

    def show_email(self, name):
        record = self.data.get(name)
        if record and record.email:
            return record.email.value
        else:
            return "No email"

    def show_address(self, name):
        record = self.data.get(name)
        if record and record.address:
            return record.address.value
        else:
            return "No address"

    def show_notes(self, name):
        record = self.data.get(name)
        if record:
            return '; '.join(note.value for note in record.notes)

    def show_all(self):
        if not self.data:
            return "Contacts were not added"
        return self.data.values()


    def find_contacts(self, search_query):
        search_results = []
        is_phone = search_query.isdigit()

        for record in self.data.values():
            if is_phone:
                # Search by phone
                if any(search_query in phone.value for phone in record.phones):
                    search_results.append(record)
            else:
                # Search by name
                if search_query.lower() in record.name.value.lower():
                    search_results.append(record)
        return search_results



def show_birthdays_in_period_handler(args):
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


# Decorators
def save_data(obj_to_save, file_name):
    def wrapper(func):
        def inner_wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            usr_dir = os.path.expanduser("~")
            file_path = os.path.join(usr_dir, file_name)
            with open(file_path, "wb") as file:
                pickle.dump(obj_to_save, file)
            return result

        return inner_wrapper

    return wrapper


def get_address_book(file_name):
    usr_dir = os.path.expanduser("~")
    file_name = os.path.join(usr_dir, "ab_data.bin")

    try:
        with open(file_name, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


# Handlers
file_name = "ab_data.bin"
book = get_address_book(file_name)


@save_data(book, file_name)
def add_handler(args):
    if len(args) != 3:
        return "Invalid command usage: add <name> <phone>"
    name, phone = args[1:]
    record = Record(name)

    try:
        if not Phone(phone).validate():
            raise ValueError("Invalid phone number")
    except ValueError:
        return "Invalid phone number. Please try again."
    
    record.add_phone(phone)
    book.add_record(record)
    return f"Contact {name} added"


@save_data(book, file_name)
def change_handler(args):
    if len(args) != 3:
        return "Invalid command usage: change <name> <new_phone>"
    name, new_phone = args[1:]
    try:
        # Validate the new phone number
        Phone(new_phone)
    except ValueError:
        return "Invalid phone number. Please try again."
    
    book.change_phone(name, new_phone)
    return f"Phone number for {name} changed"


def search_handler(args):
    if len(args) != 2:
        return "Invalid command usage: phone <query>"
    query = args[1]
    contacts = book.find_contacts(query)
    if contacts:
        print_contacts_table(contacts)
        return ''
    else:
        return "No contacts found"


# New handler for changing address
def change_address_handler(args):
    if len(args) < 3:
        return "Invalid command usage: change_address <name> <new_address>"
    command = ' '.join(args)
    parts = command.split(" ", 2)
    name, new_address = parts[1:]
    contact = book.find(name)
    if contact:
        contact.add_address(new_address)
    return f"Address for {name} changed to {new_address}"



# New handler for changing email
def change_email_handler(args):
    if len(args) != 3:
        return "Invalid command usage: change_email <name> <new_email>"
    name, new_email = args[1:]
    book.change_email(name, new_email)
    return f"Email for {name} changed"


# New handler for deleting a record
def delete_handler(args):
    if len(args) != 2:
        return "Invalid command usage: delete <name>"
    name = args[1]
    if book.find(name):
        book.delete(name)
        return f"Contact {name} deleted"
    else:
        return f"Contact {name} not found"


def all_handler(args):
    result = book.show_all()
    if result != "Contacts were not added":
        print_contacts_table(result)
        return ''
    else:
        return result


@save_data(book, file_name)
def add_address_hadler(args):
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


@save_data(book, file_name)
def add_email_handler(args):
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


@save_data(book, file_name)
def add_birthday_handler(args):
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


def show_birthday_handler(args):
    if len(args) != 2:
        return "Invalid command usage: show-birthday <name>"
    name = args[1]
    contact = book.find(name)
    if contact and contact.birthday:
        return f"Birthday for {name}: {contact.birthday}"
    else:
        return f"Contact {name} does not have a birthday or not found"


def show_birthdays_next_week_handler(args):
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


# Added show email handler
def show_email_handler(args):
    if len(args) != 2:
        return "Invalid command usage: show_email <name>"
    name = args[1]
    email = book.show_email(name)
    if email:
        return f"Email for {name}: {email}"
    else:
        return f"No email found for {name}"


# Added show address handler
def show_address_handler(args):
    if len(args) != 2:
        return "Invalid command usage: show_address <name>"
    name = args[1]
    address = book.show_address(name)
    if address:
        return f"Address for {name}: {address}"
    else:
        return f"No address found for {name}"


# Added delete handler
def delete_handler(args):
    if len(args) != 2:
        return "Invalid command usage: delete <name>"
    name = args[1]
    if book.find(name):
        book.delete(name)
        return f"Contact {name} deleted"
    else:
        return f"Contact {name} not found"



@save_data(book, file_name)
def add_note_handler(args):
    if len(args) != 3:
        return "Invalid command usage: add-note <name> <note>"
    name, note = args[1:]
    contact = book.find(name)
    if contact:
        contact.add_note(note)
        return f"Note added for {name}"
    else:
        return f"Contact {name} not found"


@save_data(book, file_name)
def edit_note_handler(args):
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


def show_note_handler(args):
    if len(args) != 2:
        return "Invalid command usage: note <name>"
    name = args[1]
    return book.show_notes(name) or f"Contact {name} not found"


@save_data(book, file_name)
def delete_note_handler(args):
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


def help_handler(args):
    print_help()
    return ''


def close_handler(args = None):
    print("Goodbye! 🛸")
    print(get_alien())
    exit(0)


handlers = {
    'add': add_handler,
    'change-number': change_handler,
    'find': search_handler,
    'all': all_handler,
    'add-birthday': add_birthday_handler,
    'show-birthday': show_birthday_handler,
    'birthdays-in-period': show_birthdays_in_period_handler,
    'birthdays': show_birthdays_next_week_handler,
    'add-address': add_address_hadler,
    'add-email': add_email_handler,
    "change-email": change_email_handler,
    "change-address": change_address_handler,
    "show-email": show_email_handler,
    "show-address": show_address_handler,
    "delete-contact": delete_handler,
    'add-note': add_note_handler,
    'edit-note': edit_note_handler,
    'note': show_note_handler,
    'delete-note': delete_note_handler,
    'help': help_handler,
    'close': close_handler,
    'exit': close_handler,
}


print_app_intro()
print("Welcome to the Address Book Assistant X!")
print_help()
try:
    while True:
        command = input("Enter a command >>>  ").split()
        if command:
            handler = handlers.get(command[0])
            if handler:
                print(handler(command))
            else:
                print("Unknown command")
        else:
            print("Please enter a command.")

except KeyboardInterrupt:
    close_handler()
