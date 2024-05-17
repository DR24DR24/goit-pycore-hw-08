
import addressbookclasses
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return addressbookclasses.AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)

    return inner

def parse_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print("cann't parse, input command please")
            return "",""

    return inner

# def change_error(func):
#     def inner(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except KeyError:
#             return "user absent"
#             #return "no such user"
#         except ValueError:
#             return "please input <change user_name>"    
#     return inner

# def phone_error(func):
#     def inner(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except KeyError:
#             return "no such user"
#         except IndexError:
#             return "please input phone + user name"

#     return inner




#birthdays
def birthdays(args, book):
    l=book.get_upcoming_birthdays() # реалізація
    return l

#show-birthday [ім'я]: 
@input_error
def show_birthday(args, book):
    if len(args)<1:
        raise ValueError("show-birthday [name]")
    name,  *_ = args
    record:addressbookclasses.Record = book.find(name)
    if record==None:
        raise Exception("No such user")
    return f"birthday: {record.birthday}"

#add-birthday [ім'я] [дата народження]    
@input_error
def add_birthday(args, book):
    if len(args)<2:
        raise ValueError("Format: add-birthday [name] [birthday]")
    name, birthday,  *_ = args
    record:addressbookclasses.Record = book.find(name)
    if record==None:
        raise Exception("No such user")
    record.add_birthday(birthday)
    return "Birthday added "

#phone [ім'я]:
@input_error
def phone_contact(args, book:addressbookclasses.AddressBook):
    if len(args)<1:
        raise ValueError("Format: phone [name]")
    name,  *_ = args
    record:addressbookclasses.Record = book.find(name)
    if record==None:
        raise Exception("No such user")
    return f"phones: {'; '.join(p.value for p in record.phones)}"

#change [ім'я] [старий телефон] [новий телефон]
@input_error
def change_contact(args, book:addressbookclasses.AddressBook):
    if len(args)<3:
        raise ValueError("Format: change [name] [old phone] [new phone]")
    name, old_phone,new_phone, *_ = args
    record:addressbookclasses.Record = book.find(name)
    if record==None:
        raise Exception("No such user")
    record.edit_phone(old_phone,new_phone)
    return "phone changed"


@input_error
def add_contact(args, book: addressbookclasses.AddressBook):
    #print(type(args))
    if len(args)<2:
        raise ValueError("Format: add [name] [phone]")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = addressbookclasses.Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@parse_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(phone_contact(args, book)) 

        elif command == "all":
            for name, record in book.data.items():
                print(record)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))# реалізація

        elif command == "birthdays":
            b=birthdays(args, book)# реалізація
            for x in b:
                print(f"Name: {x['name']}, congratulation date: {x['congratulation_date']}" ) 

        else:
            print("Invalid command.")


if __name__=="__main__":
    main()

    

