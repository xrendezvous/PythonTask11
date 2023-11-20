from collections import UserDict


class AddressBook(UserDict):
    def __str__(self):
        pass

    def add(self):
        pass

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

