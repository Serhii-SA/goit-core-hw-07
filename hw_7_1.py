# Ісходнік для ДЗ

from collections import UserDict
from datetime import datetime
from datetime import date
from datetime import timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Birthday(Field):
    def __init__(self, value:str): #Date format (DD.MM.YYYY)
        
        try:
            y=int(value[6:10]); m=int(value[3:5]); d=int(value[0:2])
            date(y,m,d)
            user_date = datetime.strptime(value, "%d.%m.%Y")
            self.value = user_date
            #return self.user_date
             
            # Додайте перевірку коректності даних
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        


class Phone(Field):
		pass

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday {self.birthday}"

    def add_phone(self,ph_num_to_add):
        if len(ph_num_to_add)== 10:
            self.phones.append(Phone(ph_num_to_add))
        else:
            print("Phonenumber has invalid format")

    def add_birthday(self,b_day):
         self.birthday=Birthday(b_day)

    def remove_phone(self,ph_num_to_del):
        if len(ph_num_to_del)== 10:
            pos=0
            for n_del in self.phones:
                if ph_num_to_del == n_del.value:
                    self.phones.pop(pos)
                else:
                    pos +=1
            print(f"No < {ph_num_to_del} > in this contact")
        else:
            print("Phonenumber has invalid format")

    def edit_phone(self,*args):
        for a in args:
            if len(a)== 10:
                self.phones.append(Phone(a))
            else:
                print("Phonenumber has invalid format") 

    def find_phone(self,str_nb):
        for n in self.phones:
            if n.value == str_nb:
                return str_nb                  
        print(f"Contact {self.name} doesn`t consists {str_nb}")
    
class AddressBook(UserDict):
        def add_record(self,cont):
              self.data.update([(cont.name,cont)])
        def show_all(self):
            for name, record in self.data.items():
                print(record)    
        def find(self,nm):
                for name, record in self.data.items():
                    if name.value == nm :
                        return record
                print(f"No < {nm} > contact in the phonebook")
        def delete(self,nm):
            for name, record in self.data.items():                
                if name.value == nm :
                    n_del = name
            try:         
                self.data.pop(n_del)
            except Exception:
                print(f"No < {nm} > contact in the phonebook") 
        def get_upcoming_birthdays(self):
            dt_tday=datetime.today().date()  #сьог.дата
            prg_out = [] # порожн.список в який засунемо вихідні словники  (ключ name) та дату привітання (ключ congratulation_date, дані якого у форматі рядка 'рік.місяць.дата'). 
            for name, record in self.data.items():
                crnt_us_nm = name.value
                print(record.birthday.value)
                print(dt_tday)
                user_brday = record.birthday.value #зі словника витягає ДР клієнта та робить об.дататайм
                user_brday_crn_year=user_brday.replace(year=dt_tday.year) # замінюєм рік в ДР на поточн.
                print(user_brday_crn_year)
                delta = user_brday_crn_year.toordinal()-dt_tday.toordinal() # визначаємо різницю в дн.між ДР та поточн.датою знак(-) -ДР вже був
                print(delta)
                if 0<= delta < 8 : # якщо ДР клієнта в найближчі 7днів
                    week_d = user_brday_crn_year.weekday() # визначаємо день тижня
                    print(week_d)
                    if 0<= week_d<5 : # якщо ДР у робочий день
                        cr_lst_conday =[crnt_us_nm,user_brday_crn_year.strftime("%Y.%m.%d")]
                        #prg_out.append(cr_dic_conday)
                    elif week_d==5: # якщо ДР у сб
                        us_bdsd_repl = user_brday_crn_year + timedelta(days=2)
                        cr_lst_conday =[crnt_us_nm,us_bdsd_repl.strftime("%Y.%m.%d")]
                        #prg_out.append(cr_dic_conday)
                    else: # решта тоді ДР у нд
                        us_bdsd_repl = user_brday_crn_year + timedelta(days=1)
                        cr_lst_conday =[crnt_us_nm, us_bdsd_repl.strftime("%Y.%m.%d")]
                    prg_out.append(cr_lst_conday)
                elif delta < 0: # якщо ДР вже минув
                    us_bdsd_repl = user_brday_crn_year.replace(year=dt_tday.year+1) # додаємо 1рік до дня привітання
                    cr_lst_conday =[crnt_us_nm, us_bdsd_repl.strftime("%Y.%m.%d")]
                    prg_out.append(cr_lst_conday)
            return prg_out



         
book=AddressBook()

j_record = Record("John")
j_record.add_phone("1234567890")
j_record.add_birthday("02.03.2018")
# jul_record.add_phone("5555555555") 
book.add_record(j_record)
#print(j_record)


jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("28.02.2010")
book.add_record(jane_record)

# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")



# for name, record in book.data.items():
#     print(record)

# # Спосіб виведення контактів завдяки  методу самої тел.книги
book.show_all() 
print(book.get_upcoming_birthdays())

# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  

# book.delete("Jane")

# book.show_all()

# jul_record = Record("Jul")
# jul_record.add_phone("1234567890")
# jul_record.add_phone("5555555000") 
# book.add_record(jul_record)

# book.show_all()

# jul_record.remove_phone("1234567891") # спроба видалити неіснуючий номер
# jul_record.remove_phone("1234567890")
# book.add_record(jul_record)
# book.show_all()