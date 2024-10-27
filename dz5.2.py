from datetime import datetime, timedelta

def input_error(handler):
   
    def wrapper(*args, **kwargs):
        try:
            return handler(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            return f"Error: {e}"
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) not in (10, 12):
            raise ValueError("Неправильний формат номера телефону.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Неправильний формат дати. Використовуйте формат ДД.ММ.РРРР")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return "Номер телефону змінено."
        return "Старий номер телефону не знайдено."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_record(self, record):
        self.contacts[record.name.value] = record

    def get_upcoming_birthdays(self, days=7):
        today = datetime.now().date()
        upcoming_birthdays = {}
        
        for record in self.contacts.values():
            days_to_birthday = record.days_to_birthday()
            if days_to_birthday is not None and 0 <= days_to_birthday <= days:
                upcoming_birthdays[record.name.value] = days_to_birthday
        
        return upcoming_birthdays

def parse_input(user_input):
    
    parts = user_input.strip().split()
    command = parts[0].lower()
    args = parts[1:]
    return command, args

@input_error
def add_contact(args, book):
    name, phone = args[0], args[1]
    record = book.contacts.get(name)
    message = "Контакт оновлено."
    if not record:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.contacts.get(name)
    if record:
        return record.change_phone(old_phone, new_phone)
    return "Контакт не знайдено."

@input_error
def show_phones(args, book):
    name = args[0]
    record = book.contacts.get(name)
    if record:
        phones = ', '.join([phone.value for phone in record.phones])
        return f"Телефони контакту {name}: {phones}"
    return "Контакт не знайдено."

@input_error
def show_all_contacts(book):
    if not book.contacts:
        return "Адресна книга порожня."
    return "\n".join([f"{name}: {', '.join([phone.value for phone in record.phones])}" for name, record in book.contacts.items()])

@input_error
def add_birthday(args, book):
    name, date = args
    record = book.contacts.get(name)
    if record:
        record.add_birthday(date)
        return f"День народження для контакту {name} додано."
    return "Контакт не знайдено."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.contacts.get(name)
    if record and record.birthday:
        return f"День народження {name}: {record.birthday.value.strftime('%d.%m.%Y')}"
    elif record:
        return "Для цього контакту день народження не встановлено."
    return "Контакт не знайдено."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "Немає контактів з днями народження на наступному тижні."
    return "\n".join([f"{name} через {days} днів" for name, days in upcoming_birthdays.items()])

def main():
    book = AddressBook()
    print("Ласкаво просимо до бота-помічника!")
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Чим можу допомогти?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phones(args, book))

        elif command == "all":
            print(show_all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Невірна команда.")