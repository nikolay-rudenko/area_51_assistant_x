from collections import UserDict
import datetime
import os
import pickle
import re


class Field:
    """
    Base class for representing various types of contact data.

    Attributes:
        value: Variable that holds the value of the given type.

    Methods:
        __str__(): Converts the field value to a string.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """
    Subclass of Field for storing the name of a contact.
    """

    pass


class Note(Field):
    """
    Subclass of Field for storing a note or comment about a contact.
    """

    pass


class Phone(Field):
    """
    Subclass of Field for storing the phone number of a contact.

    Attributes:
        value: Variable that holds the phone number.

    Methods:
        __init__(): Phone number initialization, with validation.
        validate(): Check if the phone number is in 10-digit format.
    """

    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            raise ValueError("Invalid phone number")

    def validate(self):
        return len(self.value) == 10 and self.value.isdigit()


class Address(Field):
    """
    Subclass of Field for storing the address of a contact.
    """

    pass


class Email(Field):
    """
    Subclass of Field for storing the email address of a contact.

    Attributes:
        value: Variable that holds the email.

    Methods:
        __init__(): Email initialization, with validation.
        validate(): Check email for compliance with the standard format.
    """

    def __init__(self, value):
        super().__init__(value)
        if not self.validate():
            self.value = None

    def validate(self):
        pattern = r'^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$'
        return re.match(pattern, self.value) is not None


class Birthday(Field):
    """
    Subclass of Field for storing the date of birth of a contact.

    Attributes:
        value: Variable that holds the date of birth.

    Methods:
        __init__(): Date of birth initialization, with validation.
        validate(): Check if the date of birth is in DD.MM.YYYY format.
    """

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
    This class describes an entry in the address book.

    Attributes:
        name (Name): Contact name.
        phones (list): List of phone numbers for the contact.
        birthday (Birthday): Contact's date of birth.
        address (Address): Contact's address.
        email (Email): Contact's email address.
        notes (list): List of notes about the contact.

    Methods:
        add_phone(phone_number: str): Add a phone number to the phone list.
        remove_phone(phone_number: str): Remove a phone number from the list.
        edit_phone(old_number: str, new_number: str): Change a phone number in the list.
        find_phone(phone_number: str): Find a phone number in the list.
        add_birthday(birthday: datetime.date): Add date of birth.
        days_to_birthday(): Calculate days until birthday.
        show_notes(): Show all notes.
        add_note(note: str): Add a note.
        edit_note(note_index: int, new_note: str): Edit a note.
        remove_note(note_index: int): Delete a note.
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
    This class represents the entire address book.

    Attributes:
        data (dict): Dictionary where the key is the contact's name, and the value is an instance of the Record class.

    Methods:
        add_record(record: Record): Adds a record to the address book.
        find(name: str): Finds a record by name.
        delete(name: str): Deletes a record by name.
        change_phone(name: str, new_phone: str): Changes a contact's phone number.
        change_email(name, new_email): Changes a contact's email address.
        change_address(name, new_address): Changes a contact's address.
        show_phone(name: str): Displays a contact's phone number(s).
        show_email(name: str): Displays a contact's email address.
        show_address(name: str): Displays a contact's address.
        show_notes(name: str): Displays a contact's notes.
        show_all(): Displays all records in the address book.
        find_contacts(search_query): Finds contacts based on their name or phone number.
    """


    # def __init__(self):
    #     super().__init__()
    #     # restore data from file
    #     usr_dir = os.path.expanduser("~")
    #     file_path = os.path.join(usr_dir, "ab_data.bin")
    #     try:
    #         with open(file_path, "rb") as file:
    #             self.data = pickle.load(file)
    #     except FileNotFoundError:
    #         self.data = {}


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
            if record.notes:
                return '; '.join(note.value for note in record.notes)
            else:
                return "No notes found for this contact"
        else:
            return f"Contact {name} not found"

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
