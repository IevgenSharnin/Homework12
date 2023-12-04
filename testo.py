from collections import UserDict
from datetime import datetime
import pickle
# Клас-"батько" для кожного поля у довіднику
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

    def __str__(self):
        return str(self.value)
# Клас для імені контакта - зберігаємо з першою великою літерою
class Name(Field):
    def __init__(self, value):
        self.value = value.title()
# Клас для дня народження контакта - перевірка на формат "ДД.ММ.РРРР"
class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value (self, new_value):
        try:
            self._Field__value = datetime.strptime (new_value, '%d.%m.%Y').date()
        except:
            raise ValueError ('Wrong format for birthday')
# Клас для номера телефона контакта - перевірка на значення 10 цифр
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value (self, new_value):
        if (len (new_value) != 10) or (not new_value.isdigit()):
            raise ValueError ('Phone number should have 10 digit.')
        else:
            self._Field__value = new_value
# Клас для усього запису довідника: ім'я + телефони(кілька) + день народження
# Плюс розрахунок дней до наступної дати народження плюс принтування запису
class Record:
    def __init__(self, name, birthday=0):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def add_birthday (self, b_day):
        try:
            self.birthday = Birthday (b_day)
        except:
            return print (f"Birthday '{b_day}' not added.\n")
        print (f"Birthday for '{self.name.value}' added.\n")

    def add_phone (self, phone):
        try:
            phone_checked = Phone (phone)
        except:
            return print (f"Phone number '{phone}' not added.\n")
        self.phones.append (phone_checked)
        print (f"Phone number for '{self.name.value}' added.\n")

    def remove_phone (self, phone):
        try:
            phone_checked = Phone (phone)
        except:
            return print (f"Phone number '{phone}' not removed.\n")
        print (self.phones)
        for phone_for_check in self.phones:
            if phone_checked.value == phone_for_check.value:
                self.phones.remove (phone_for_check)
            return print ("Phone number for deleted\n")

    def edit_phone (self, phone1, phone2):
        for exist_phone in self.phones:
            if phone1 == exist_phone.value:
                self.phones.remove (exist_phone)
                phone_checked = Phone (phone2)
                if phone_checked:
                    self.phones.append (phone_checked)
                    return f"Phone number for '{self.name.value}' edited\n"
        raise ValueError

    def find_phone (self, phone):
        for find_phone in self.phones:
            if phone == find_phone.value:
                return find_phone
        print (f"'{self.name.value}' don't have phone number, what you want to find\n")

    def days_to_birthday (self):
        if self.birthday == 0:
            raise ValueError
        if datetime.today().date() < self.birthday.value:
            next_birthday = self.birthday.value
            days_to_next = next_birthday - datetime.today().date()
        elif datetime.today() < datetime (datetime.today().year, \
                        self.birthday.value.month, self.birthday.value.day):
            next_birthday = datetime (datetime.today().year, \
                        self.birthday.value.month, self.birthday.value.day)
            days_to_next = next_birthday.date() - datetime.today().date()
        else:
            next_birthday = datetime (datetime.today().year + 1, \
                        self.birthday.value.month, self.birthday.value.day)
            days_to_next = next_birthday.date() - datetime.today().date()
        return days_to_next.days

    def __str__(self):
        try:
            return f"Contact name: {self.name._Field__value}; \
phones: {', '.join(p.value for p in self.phones)}; birthday: {self.birthday}"
        except AttributeError:
            return f"Contact name: {self.name._Field__value}; phones: no phones added; birthday: {self.birthday}"
# Клас для усієї книжки: 
# керування записами + видача порцій записів для посторінкового друку
class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
        self.count_for_print = 0

    def add_record (self, record: Record):
        self.data.update ({record.name.value: record})
        print (f"Contact '{record.name.value}' added\n")
#        print (f'dict from class: {self.data}')
#        with open ('phonebook.bin', 'ab') as file:
#            one_record = pickle.dumps (record)
#            file.write (one_record)
#            file.write (b'\n')
#        with open ('phonebook.bin', 'rb') as file:
#            file_readed = pickle.load (file)
#            print (f'from pickle: {file_readed}')
#            print (f'as lines: {file.readlines()}')
#            file.seek(0)
#            phonebook_readed = {}
#            while True:
#                line_ = file.readline()
#                line = pickle.loads (line_[:-1])
#                print (f'line: {line}')
#                if line:
#                    phonebook_readed.update (line)
#                else: break
#            print (f'as file: {phonebook_readed}')

    def find (self, name):
        self.name = Name (name)
        return self.data.get (self.name.value)

    def delete (self, record: str):
        if self.data.get (record):
            record_deleted = self.data.pop (record)
            print (f"Contact '{record_deleted}' deleted\n")
        else:
            print (f"Contact book don't have contact '{record}'\n")
    
    def __next__(self):
        if not self.count_for_print:
            while True:
                number_records_on_page = input ('How many records on page do you want? ')
                self.number_records_on_page = number_records_on_page
                if self.number_records_on_page.isdigit():
                    break
        records_on_page = {}
        if self.count_for_print < len (self.data):
            for _ in range (0, int(self.number_records_on_page)):
                if self.count_for_print < len (self.data):
                    records_on_page [list (self.data.keys()) [self.count_for_print - 1]] =\
                                self.data [list (self.data.keys()) [self.count_for_print - 1]]
                    self.count_for_print += 1
            return records_on_page
        raise StopIteration
# Клас-"ітератор" для посторінкового друку
class PrintIterator:
    def __init__(self, addr_book: AddressBook):
        self.addr_book = addr_book

    def __iter__(self):
        return self.addr_book

if __name__ == "__main__":
# Тестово читаємо книжку з телефонами
    print ("-----Тестово читаємо книжку з телефонами-----")
    try:
        with open ('phonebook.bin', 'rb') as file:
            book = pickle.load (file)

        print (book)
        for record in book.values():
            print (record)
# Створення нової адресної книги, якщо не було файлу
    except FileNotFoundError:
        book = AddressBook()


# Виведення всіх записів у книзі
    print ('-----Виведення всіх записів у книзі-----')
    print (book)
    print (type(book))
    pages_to_print = PrintIterator(book)
    page = 1
    for records_on_page in pages_to_print: #book.data.items():
        print (f'--- Page {page} ---')
        page += 1
        for record in records_on_page.values():
            print(record)
            try:
                print(f"Days to next {record.name}'s birthday: {record.days_to_birthday()}\n")
            except ValueError:
                print ('')
            except AttributeError:
                print(f"I can't calculate days to next b-day for date {record.birthday}")
        if book.count_for_print < len (book.data):
            input ('\nPress Enter for print next page\n')
        else:
            print (f'--- End of book ---')
    print ('')

# Знаходження та редагування телефону для John
#    print ('-----Знаходження та редагування телефону для John-----')
#    john = book.find("john")
#    john.edit_phone("1234567890", "1112223333")

#    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
#    print ('-----Пошук конкретного телефону у записі John-----')
#    found_phone = john.find_phone("5555555555")
#    print(f"{john.name}: {found_phone}\n")  # Виведення: 5555555555

    # Видалення запису Jane
#    print ('-----Видалення запису Jane-----')
#    jane11 = book.find("jane")
#    print (jane11, '- found jane11')
#    book.delete("Jane")
#    jane22 = book.find("Jane")
#    print (jane22, '- found jane22')

# Записуємо творчість у файл перед закінченням роботи
    print ("-----Записуємо творчість у файл перед закінченням роботи-----")
    with open ('phonebook.bin', 'wb') as file:
        pickle.dump (book, file)
#        file.write (one_record)
#        file.write (b'\n')
#        with open ('phonebook.bin', 'rb') as file:
#            file_readed = pickle.load (file)
#            print (f'from pickle: {file_readed}')
#            print (f'as lines: {file.readlines()}')
#            file.seek(0)
#            phonebook_readed = {}
#            while True:
#                line_ = file.readline()
#                line = pickle.loads (line_[:-1])
#                print (f'line: {line}')
#                if line:
#                    phonebook_readed.update (line)
#                else: break
#            print (f'as file: {phonebook_readed}')
# without file
#{'John': <__main__.Record object at 0x000002B9EE9F8610>,
#'Jane': <__main__.Record object at 0x000002B9EEF25490>, 
#'John&Jane': <__main__.Record object at 0x000002B9EEF910D0>, 
#'Jane&John': <__main__.Record object at 0x000002B9EEF902D0>}