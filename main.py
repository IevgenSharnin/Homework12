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
        self.stringets = ''

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
            self.stringets = f"Contact name: {self.name._Field__value}; \
#phones: {', '.join(p.value for p in self.phones)}; birthday: {self.birthday}"
#            return print ('|{:<15}|{:<35}|{:<12}|'.format(self.name._Field__value, ", ".join(p.value for p in self.phones), self.birthday))
            return self.stringets
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
                number_records_on_page = input ('How many records on page do you want to print? ')
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
    print ("-----Читаємо книжку з телефонами з файлу, якщо він є-----")
    try:
        with open ('phonebook.bin', 'rb') as file:
            book = pickle.load (file)
# Обнуляю каунтер для посторінкового друку, щоб не маратися з __getstate__
        book.count_for_print = 0
# Створення нової адресної книги, якщо не було файлу
    except FileNotFoundError:
        book = AddressBook()

# Створення запису для John
    print ('-----Створення запису для John-----')
    john_record = Record("john")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("10.02.2021")

# Додавання запису John до адресної книги
    print ('-----Додавання запису John до адресної книги-----')
    book.add_record(john_record)

# Створення та додавання нового запису для Jane
    print ('-----Створення та додавання нового запису для Jane-----')
    jane_record = Record("jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

# Створення запису для John&Jane
    print ('-----Створення запису для John&Jane-----')
    jo_ja_record = Record("John&Jane")
    jo_ja_record.add_phone("1236547890")
    jo_ja_record.add_phone("6666666666")
    jo_ja_record.add_birthday("10.02.2025")
    book.add_record(jo_ja_record)

# Створення запису для Jane&John
    print ('-----Створення запису для Jane&John-----')
    ja_jo_record = Record("Jane&John")
    ja_jo_record.add_phone("9999999999")
    ja_jo_record.add_phone("7777777777")
    ja_jo_record.add_birthday("10.12.2021")
    book.add_record(ja_jo_record)

# Виведення всіх записів у книзі по сторінках
    print ('-----Виведення всіх записів у книзі по сторінках-----')
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

# Виведення всіх записів у книзі, що відповідають пошуку
    for_find = input ('Please enter symbols for find name and phone numbers in phone book: ')
    print (f"-----Виведення всіх записів у книзі із рядком '{for_find}'-----")
    for record in book.data.values():
        if record.stringets.find (for_find) != -1:
            print(record)
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
    with open ('phonebook.bin', 'wb') as file:
        pickle.dump (book, file)
