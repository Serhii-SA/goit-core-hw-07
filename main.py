# Незакінченне ДЗ 07

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

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "You didn't attached the Name and phone nbr or attached too many arg-s.\nGive me name and phone please."
        except KeyError:
            nm = args[0]
            return print(f"No user with name - {nm[0]}")
    return inner

text= ''' 
"add username phone".

 За цією командою бот зберігає у пам'яті, 
новий контакт. Користувач вводить ім'я username та номер телефону phone, обов'язково через пробіл.

"change username phone"
За цією командою бот зберігає в пам'яті новий номер телефону phone для 
контакту username, що вже існує в записнику.

"phone username"
 За цією командою бот виводить у консоль номер телефону для зазначеного контакту username.

"all"
 За цією командою бот виводить всі збереженні контакти з номерами телефонів у консоль.

"close", "exit"
 за будь-якою з цих команд бот завершує свою роботу
 '''

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
#add f 0123456789 
@input_error
def add_contact(args, contacts):
    nme, phone = args

    for n in contacts.data:
        # print(n)
        if nme == n.value:
            return print(f"Contact with name {nme} is already exists.If you'd like to change it, use command 'change'")
    #if 1<len(args)<3:
    #else:    
    r=Record(nme)
    r.add_phone(phone)
    contacts.add_record(r)
    return print("Contact added.")
    #else:
        #return "Invalid input"

@input_error
def chng_contact(args, contacts):    
        nme, phone = args
        for n in contacts.data:
            if nme == n.value:
                temp_rec=contacts.find(nme)
                temp_bd=temp_rec.birthday
                contacts.delete(nme)
                r=Record(nme)
                r.add_phone(phone)
                if temp_bd != None:
                    r.add_birthday(temp_bd.strftime("%d.%m.%Y"))
                contacts.add_record(r)
                return print(f"Contact {nme} phone changed")
        return print(f"Contact {nme} phone number doesn`t exist.")
    #else:
        #return "Invalid input"   
@input_error
def all_contact(contacts):
    if contacts == {}:
        print("\nContacts list is empty.\n")
    else:
        for key in contacts:
            print(key,contacts[key])

@input_error
def usn_ph(args, contacts):
    #try:
    return print(args[0],contacts[args[0]])
    #except:
        #print(f"No user with name - {args[0]}")
    
        
def main():
    contacts = AddressBook()

    print("Welcome to the assistant bot!\n(\"Help\"-for help)")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")

            break



        elif command == "hello":
            print("How can I help you?(\"Help\"-for help)")
        elif command == "add":
            add_contact(args, contacts)
        elif command == "all":
            all_contact(contacts)
        elif command == "change":
            chng_contact(args, contacts)
        elif command == "phone":
            usn_ph(args, contacts) 
        elif command == "help":
            print(text)           
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()

