# Address Book Assistant

The Address Book Assistant is a console-based application for managing contact information. It allows users to add, modify, and search for contacts. Each contact can include details such as name, phone number, address, email, birthday, and notes.

## Features

- **Contact Management**: Add, delete, and modify contact information.
- **Birthday Alerts**: Check for upcoming birthdays within a specified period.
- **Notes**: Attach notes to contacts for additional information.
- **Persistence**: Save and load contact information using pickle for data persistence.

## Installation

No installation is required. Ensure you have Python 3.x installed on your system to run the script.

## Usage

To use the Address Book Assistant, run the script in your terminal or command prompt:

```bash
python assistant_x.py
```
### Commands

* Add Contact: add <name> <phone>
* Change Phone: change <name> <new_phone>
* Add Birthday: add-birthday <name> <DD.MM.YYYY>
* Add Address: add-address <name> <address>
* Add Email: add-email <name> <email>
* Add Note: add-note <name> <note>
* Edit Note: edit-note <name> <note_index> <new_note>
* Delete Note: delete-note <name> <index>
* Show Phone: phone <name>
* Show All Contacts: all
* Show Contact's Notes: note <name>
* Show Contact's Birthday: show-birthday <name>
* Find Upcoming Birthdays: birthdays-in-period <days>
* Exit: exit or close

### Example

#### To add a new contact:

`add John 1234567890`

#### To change a phone number for an existing contact:
`change John 0987654321`

#### To add a birthday to a contact:
`add-birthday John 01.01.1990`

### Data Persistence
The application automatically saves your address book data to a file named ab_data.bin in the user's home directory. The data is loaded from this file when the application starts.

### Contributing

Feel free to fork the repository and submit pull requests to contribute to the development of the Address Book Assistant.