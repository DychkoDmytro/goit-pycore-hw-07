from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) not in (10, 12):  # Базовая проверка номера телефона
            raise ValueError("Неправильный формат номера телефона.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            # Преобразование строки даты в объект datetime
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Неправильный формат даты. Используйте формат ДД.ММ.ГГГГ")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now().date()
        next_birthday = self.birthday.value.replace(year=today.year).date()  # Преобразование в date
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