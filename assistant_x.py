from helpers import print_app_intro, print_help
from handlers import *
from models import *

file_name = "ab_data.bin"

def main():
    book = get_address_book()

    print_app_intro()
    print("Welcome to the Address Book Assistant X!")
    print_help()

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

    try:
        while True:
            command = input("Enter a command >>>  ").split()

            if command:
                handler = handlers.get(command[0])
                if handler:
                    print(handler(command, book = book))
                else:
                    print("Unknown command")
            else:
                print("Please enter a command.")
    except KeyboardInterrupt:
        close_handler()


if __name__ == "__main__":
    main()
