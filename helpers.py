from colorama import Fore, Back, Style


def print_contacts_table(contact_list):
    result = [["Name", "Phone Numbers", "Birthday", "Address", "Email"]]
    for contact in contact_list:
        result.append(
            [
                contact.name.value,
                ", ".join(list(map(lambda x: x.value, contact.phones))),
                contact.birthday,
                contact.address,
                contact.email,
            ]
        )
    pretty_print_table(result)


def print_help():
    print("Available commands:")
    commands = [
        ["all", "Show all contacts."],
        ["add <name> <phone>", "Add a new contact."],
        ["change <name> <new_phone>", "Change the phone number for a contact."],
        ["find <query>", "Search for a contact by name or phone number."],
        ["add-birthday <name> <birthday>", "Add birthday for a contact"],
        ["show-birthday <name>", "Show the birthday for a contact."],
        [
            "birthdays-in-period <days>",
            "Show upcoming birthdays in the specified period.",
        ],
        ["birthdays", "Show birthdays within the next week."],
        ["add-address <name> <address>", "Add an address for a contact."],
        ["add-email <name> <email>", "Add an email for a contact."],
        ["change-email <name> <new_email>", "Change the email for a contact."],
        ["change-address <name> <new_address>", "Change the address for a contact."],
        ["show-email <name>", "Show the email for a contact."],
        ["show-address <name>", "Show the address for a contact."],
        ["delete <name>", "Delete a contact."],
        ["add-note <name> <note>", "Add a note for a contact."],
        ["edit-note <name> <note_index> <new_note>", "Edit a note for a contact."],
        ["note <name>", "Show all notes for a contact."],
        ["delete-note <name> <index>", "Delete a note for a contact."],
        ["help", "Show available commands."],
        ["close | exit", "Close the application."],
    ]
    pretty_print_table(commands, line_between_rows=False)


def pretty_print_table(rows, line_between_rows=True):
    """
    Example Output
    ┌──────┬─────────────┬────┬───────┐
    │ True │ short       │ 77 │ catty │
    ├──────┼─────────────┼────┼───────┤
    │ 36   │ long phrase │ 9  │ dog   │
    ├──────┼─────────────┼────┼───────┤
    │ 8    │ medium      │ 3  │ zebra │
    └──────┴─────────────┴────┴───────┘
    """

    # find the max length of each column
    max_col_lens = list(
        map(max, zip(*[(len(str(cell)) for cell in row) for row in rows]))
    )

    # print the table's top border
    print("┌" + "┬".join("─" * (n + 2) for n in max_col_lens) + "┐")

    rows_separator = "├" + "┼".join("─" * (n + 2) for n in max_col_lens) + "┤"

    row_fstring = " │ ".join("{: <%s}" % n for n in max_col_lens)

    for i, row in enumerate(rows):
        print("│", row_fstring.format(*map(str, row)), "│")

        if line_between_rows and i < len(rows) - 1:
            print(rows_separator)

    # print the table's bottom border
    print("└" + "┴".join("─" * (n + 2) for n in max_col_lens) + "┘")


def print_app_intro():
    print(
        Fore.GREEN
        + Style.BRIGHT
        + """
 █████╗ ███████╗███████╗██╗███████╗████████╗ █████╗ ███╗   ██╗████████╗    ██╗  ██╗
██╔══██╗██╔════╝██╔════╝██║██╔════╝╚══██╔══╝██╔══██╗████╗  ██║╚══██╔══╝    ╚██╗██╔╝
███████║███████╗███████╗██║███████╗   ██║   ███████║██╔██╗ ██║   ██║        ╚███╔╝ 
██╔══██║╚════██║╚════██║██║╚════██║   ██║   ██╔══██║██║╚██╗██║   ██║        ██╔██╗ 
██║  ██║███████║███████║██║███████║   ██║   ██║  ██║██║ ╚████║   ██║       ██╔╝ ██╗
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝       ╚═╝  ╚═╝
"""
    )


def get_alien():
    return """
                                                                                  
                                    ▄▄▄▄▄▄                                     
                          ▄▄▄█████████████████████▄▄,                           
                     ,▄███████████▓╣╢╢╢╢╣╢╢▓███████████▄▄                       
                  ▄▄███████╣╢▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣▓███████▄,                   
               ,▄██████▓╢▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╢▓██████▄                 
             ▄██████▓╢▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣╣╣╣╢▓██████,              
           ▄█████▓█╢▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣╣╣╣╣╣╢▓██████,            
          █████▓█╣╢╣╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣╣╣╣╣╣╣╢╢╢╣█▓████▄           
        ▄███████╣╢╢╣╣╣╣▓╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣╣╣╣╣╣╣╢╢╢╢╢╢▓▓█████,         
       ▄████▓██╢╢╢╢╣╣╢╣╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣▓╣╣╣╣╣╢╢╢╢╢╢▓▓▓████▄        
      ▄███████╣╢╢╢╢╢╣╣╣╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣╣╣╣╢╣╣╢╢╢╢╢╢╢╢╢▓▓▓████▄       
     ▐████████╣╢╢╢╢╢╢╢╣▓╣╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣╣╣╣╣╣╣╣╢╢╢╢╢╢╢╢╢╢╢▓▓▓▓████▄      
     ████▓▓▓██▓╢╢╢╢╢╢╢╢╢╣╣╣╣╣▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓╣╣╣╣╣╣╢╢╢╢╢╢╢╢╢╢╣╢╣╢▓▓▓▓▓████      
     ████▓▓█████▓╢╢╢╢╢╢╣╣╣╣╣╣╣╣▓╣╣╣▓╣╣╣╣╣╣▓╣╣╣╣╣╢╢╢╢╢╢╢╢╢╢╢╢╢╢╣╢▓▓▓▓▓▓▓███▌     
     ████▓▓█████▀▓▒╢╢╢╢╢╢╢╢╣╣╢╣╣╣╢╣╣╣╣╣╣╣╣╣╣╣╢╣╣╢╢╢╢╢╣╢╢╢╢╢╢╢▒▓█▓▓▓▓▓▓▓███      
      ███▓▓▓▓█▒╢╢╢╢╢╢╢╢╢╢╢╢╢╢╢╢╣╢╣╢╢╢╢╣╣╢╣╢╢╣╢╢╢╢╢╢╢╢╣╢╢╢╣╢╢╣╣╣▒▒▓▓▓▓▓████      
      ▐███▓▓▓▓██▓▒╢╢╢╢╢╣╢╢╢╣╢╢╣╣╢╣╣╢╢╣╣╢╢╣╣╣╢╢╢╢╢╢╢╢╢╢╢╢╢╣╣╢╢╢╢▒▓▓▓▓▓▓███▌      
       ████▓▓███████▓▒╢╢╢╢╢╢╢╢╣╢╢╢╣╢╣╣╢╢╣╣╢╢╢╢╢╢╣╢╢╢╢╢╢╣╢╢╢▒▓▓█▓▓▓▓▓▓███▌       
        ███████▓  ▓████▓╣╢╢╢╢╢╢╢▓▓╢╣╢╢╢╣╢╢╢╢╢╢╢▓╣╢╢╢╢╢╢▒▓▓█▓▓  ▓▓▓▓████        
         ████▓█▓     ▓███▓▒╢╢╢╢╢╢▓█▓╣╢╢╢╢╣▓▓▓▒╢╢╢╢╢▒▓██▓▓▓     ▓▓▓████         
         ╙█████         █▓███▓╢╢╢╢╢╢████████▒╢╢╢╢╣╫▓██▓█        ▓▓████          
          █████            ▓███╣╢╢╢╢╢▓████╣╢╢╢╢╢╫███▓           ▓▓▓██-          
          █████             ▓██▓╢╢╢╢╢╢██╣╢╢╣╢╢▓██▓              ▓▓▓██           
          ███▓█▓             ████▓╣╢╢╢╢╣╢╢╣╢╢▒██▓           ▓   ▓▓███           
          ▐██▓██              ████▓╢╢╢╢╢╢╢╢╢╣██▓           ▓   ▓▓▓██▌           
           ▀██▓█▓   ▓          ██▓█▌╢╢╢╢╢╢╢╢▓██           ▓   ▒▓▓███            
            ███▓█               ██▓█╣╢╢╢╢╢╢▓██           ▓   ▒▓▓███             
             ███▓█▓▒             ██▓▓╢╢╢╢╢╢███             ▀▒▓▓███              
              ███▓██▓            ████▓╣╢╢▓█████          ▀▒▓▓▓███               
               ████████▓╢▒▒      ▒▒╣╢╢╢╢╢╢╣╢▒▒▀      ▒▒▒▓▓▓▓▓███                
                ▀████▓▓█████▓▓▓▓███▓▒██╢▓█▒▓██▓▓▓▓▓▓▓█▓▓▓▓█████                 
                  ▀█████████▓▓████▓╢█▀   ▀█▒╢▓██▓█▓█████████▀▀                  
                        ▀█████████▓         ▓█████████▀▀'                       
                         ▐███████▓   ▒▒▒▒▒   ▓█▓██▓██▌                          
                          ███▓▓██▒███████████▒██▓▓███                           
                          ▀██████▓█▓▓█████▓▓█▓██████▌                           
                           `████▓█▓█████████▓█████▀                             
                              ████▓█▓▓███▓▓█▓███▀                               
                               ╙███████████████                                 
                                 ▀███▓███████▀                                  
                                   █████████                                    
                                    ▀█████▀                                     
                                                                                """
