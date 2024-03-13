from collections import UserDict
import datetime
import os
import pickle

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
            raise ValueError("Invalid email address")

    def validate(self):
        return "@" in self.value

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

    def add_email(self,email):
        self.email = Email(email)
    
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
        return next((phone for phone in self.phones if phone.value == phone_number), None)

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
        birthday_date = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)

        if birthday_date < today:  # If birthday has passed this year, calculate for next year
            birthday_date = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)

        return (birthday_date - today).days

    def __str__(self):
        return (f"Contact name: {self.name.value}, "
                f"phones: {'; '.join(p.value for p in self.phones)}"
                f", birthday: {self.birthday}" if self.birthday else "No birthday"
                f"address: {self.address}" if self.address else "No address"
                f"email: {self.email}" if self.email else "No email"
                )


class AddressBook(UserDict):
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

    def show_phone(self, name):
        record = self.data.get(name)
        if record:
            return '; '.join(phone.value for phone in record.phones)
        
    def show_notes(self, name):
        record = self.data.get(name)
        if record:
            return '; '.join(note.value for note in record.notes)

    def show_all(self):
        return '\n'.join(str(record) for record in self.data.values())

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
            birthday_month_day = (contact.birthday.value.month, contact.birthday.value.day)
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
            usr_dir = os.path.expanduser('~')
            file_path = os.path.join(usr_dir, file_name)
            with open(file_path, 'wb') as file:
                pickle.dump(obj_to_save, file)
            return result
        return inner_wrapper
    return wrapper


def get_address_book(file_name):
    usr_dir = os.path.expanduser('~')
    file_name = os.path.join(usr_dir, 'ab_data.bin')

    try:
        with open(file_name, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()

# Handlers
print("Welcome to the Address Book Assistant")
file_name = 'ab_data.bin'
book = get_address_book(file_name)

@save_data(book, file_name)
def add_handler(args):
    if len(args) != 3:
        return "Invalid command usage: add <name> <phone>"
    name, phone = args[1:]
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return f"Contact {name} added"

@save_data(book, file_name)
def change_handler(args):
    if len(args) != 3:
        return "Invalid command usage: change <name> <new_phone>"
    name, new_phone = args[1:]
    book.change_phone(name, new_phone)
    return f"Phone number for {name} changed"

def phone_handler(args):
    if len(args) != 2:
        return "Invalid command usage: phone <name>"
    name = args[1]
    return book.show_phone(name) or f"Contact {name} not found"

def all_handler(args):
    return book.show_all()

@save_data(book, file_name)
def add_address_hadler(args):
    if len(args) != 3:
        return "Invalid command usage: add_address <name> <address>"
    name, address = args[1:]
    contact = book.find(name)
    if contact:
        contact.add_address(address)
        return f"Address added for {name}"
    else:
        return f"Contact {name} not found"
@save_data(book, file_name)
def add_email_handler(args):
    if len(args) != 3:
        return "Invalid command usage: add_email <name> <email>"
    name, email = args[1:]
    contact = book.find(name)
    if contact:
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
            birthday_date = datetime.date(contact.birthday.value.year, contact.birthday.value.month, contact.birthday.value.day)
            if (birthday_date.day, birthday_date.month) >= (today.day, today.month) and (birthday_date.day, birthday_date.month) <= (next_week.day, next_week.month):
                birthdays.append(contact)
    if birthdays:
        for birthday in birthdays:
            print(f"Upcoming birthdays within the next week:\n {birthday}")
    else: 'No birthdays within the next week.'

    return ''

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

def hello_handler(args):
    return "Hello, how can I assist you today?"

def close_handler(args):
    exit(0)

handlers = {
    'add': add_handler,
    'change': change_handler,
    'phone': phone_handler,
    'all': all_handler,
    'add-birthday': add_birthday_handler,
    'show-birthday': show_birthday_handler,
    'birthdays-in-period': show_birthdays_in_period_handler,
    'birthdays': show_birthdays_next_week_handler,
    'add-address': add_address_hadler,
    'add-email': add_email_handler,
    'add-note': add_note_handler,
    'edit-note': edit_note_handler,
    'note': show_note_handler,
    'delete-note': delete_note_handler,
    'hello': hello_handler,
    'close': close_handler,
    'exit': close_handler,
}

while True:
    command = input().split()
    handler = handlers.get(command[0])
    if handler:
        print(handler(command))
    else:
        print("Unknown command")