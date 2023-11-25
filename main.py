from datetime import datetime, timedelta
from collections import UserDict


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def validate(self, value):
        if len(value) > 30:
            raise ValueError(f"Name should be no more than 30 symbols")
        if not value.isalpha():
            raise ValueError("Name should consist of letters")

    def __str__(self):
        return f"Name: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        self.__value = datetime.strptime(value, '%Y.%m.%d').date()

    def __str__(self):
        return f"Birthday: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def days_to_birthday(self):
        today = datetime.now().date()
        birthday_date = self.value.replace(year=today.year)
        if today > birthday_date:
            birthday_date = birthday_date.replace(year=today.year + 1)
        days_left = (birthday_date - today).days
        return days_left


class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number should be a 10-digit number')

    def __str__(self):
        return f"Phone: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        self.validate(value)
        self.__value = value


class Record:
    def __init__(self, name, birthday = None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def __str__(self):
        result = f"{self.name}"
        if self.phones:
            result += f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        if self.birthday:
            result += f"{self.birthday}"
        return result

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

        return None

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                self.phones[i].validate(new_phone)
                return f"Phone number {old_phone} updated to {new_phone}"

        raise ValueError(f"No phone number {old_phone} found")

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return f"Phone number {phone_number} removed"

        return f"No phone number {phone_number} found"

    def days_to_birthday(self):
        if self.birthday:
            return self.birthday.days_to_birthday()
        return None


class AddressBook(UserDict):
    def __str__(self):
        result = ""
        for name, record in self.data.items():
            result += f"{name}: {record}\n"
        return result

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted"
        else:
            return f"No record found with name {name}"

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
        if result:
            yield result


