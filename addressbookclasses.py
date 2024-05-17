
from collections import UserDict
import datetime

class PhoneError(Exception):
       pass

class BirthdayError(Exception):
     pass




class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)



class Name(Field):
    # реалізація класу
		pass



class Phone(Field):
    # реалізація класу
		pass

class Birthday(Field):
    def __init__(self, value):
        try:
            db=datetime.datetime.strptime(value,"%d.%m.%Y")
            if db>datetime.datetime.today():# Додайте перевірку коректності даних
                raise BirthdayError
            self.value=db.date()# та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        except BirthdayError:
            raise ValueError("Invalid date")
    
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self,birthday:str):
        self.birthday=Birthday(birthday)

    def add_phone(self,phone:str):
        if   not phone.isdigit() or len(phone)!=10: #Debug !=10
               raise PhoneError("Мust be 10 digit")
        self.phones.append(Phone(phone))

    def edit_phone(self,old_phone,new_phone):
        if   not new_phone.isdigit() or len(new_phone)!=10: #Debug !=10
            raise PhoneError("Мust be 10 digit")
        fo=self.find_phone(old_phone)
        if fo==None:
            raise ValueError("No such phone")
        fo.value=new_phone

        
    def find_phone(self,phone):
        phone_objects=[x for x in self.phones if x.value==phone]
        return phone_objects[0] if len(phone_objects)>0 else None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)},\
 birthday: {self.birthday}"




class AddressBook(UserDict):
    # реалізація класу
    def __init__(self):
        self.data = {}
    
    def add_record(self,record:Record):
        self.data[record.name.value]=record
        
    def find(self,user_name):
        return self.data.get(user_name)
    
    def delete(self,user_name):
        try:
            del self.data[user_name]
        except KeyError:
            print("no such user")
		
    def get_upcoming_birthdays(self, now_for_debug=None):
        upcoming_birthdays=[]
        for name,record in self.data.items():
            try:
                user_birthday=record.birthday.value
            except:
                 continue    
            
            if now_for_debug==None:                      #for debug and test
                today=datetime.date.today()
            else:
                today=now_for_debug
    
            if user_birthday.day==29 and user_birthday.month==2 and not calendar.isleap(today.year): #leap year
                user_birthday=user_birthday+datetime.timedelta(days=1)
    
            
            birthday_this_year=user_birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_actual=birthday_this_year.replace(year=birthday_this_year.year+1)
            else:
                birthday_actual=birthday_this_year
            delta_until_birthday=birthday_actual-today
            if delta_until_birthday.days<7:
                if birthday_actual.isoweekday()>5:
                    birthday_actual=birthday_actual+datetime.timedelta(days=8-birthday_actual.isoweekday())
                d={'name': name,
                   'congratulation_date': birthday_actual.strftime("%d.%m.%Y")}
                    #upcoming_birthdays.update({'name': "1",'congratulation_date': "2"})
                upcoming_birthdays=upcoming_birthdays+[d]
    
    
        upcoming_birthdays.sort(key=lambda d: d['congratulation_date'])
    
        return upcoming_birthdays



if __name__=="__main__":
# Створення нової адресної книги
    book = AddressBook()
    
        # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    
    john_record.add_birthday("19.05.2000")
    
        # Додавання запису John до адресної книги
    book.add_record(john_record)
    
        # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)
    
        # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)
    
    upcoming_birthdays=book.get_upcoming_birthdays()
    print(upcoming_birthdays)

    print(john_record.name.value)
    print(list(book.keys()))    
    
        # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    
    
    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
    
        # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
    
        # Видалення запису Jane
    book.delete("Jane")
    
        # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    

