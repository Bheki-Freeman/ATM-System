import sqlite3
from functions import logout
import logging
import queue

line = '*' * 41
conn = sqlite3.connect('main.db')
cur = conn.cursor()
stack = queue.LifoQueue()

class Customer():
    def __init__(self) -> None:
        pass
    def set_values(self, ss_number, first_name, last_name, email_address, phone_number, physical_address, username, password):
        self.ss_number = ss_number
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address
        self.phone_number = phone_number
        self.physical_address = physical_address
        self.username = username
        self.password = password
    
    def cust_menu(self):        
        print(f'{line}\n\t [CUSTOMER DASH-BOARD]\n{line}\n')
        choice = int(input('What are we doing Today:\n\t1 ---- Find Customer By SS_Number\n\t2 ---- Add New Customer\n\t3 ---- Update Customer Details'+
                           '\n\t4 ---- Delete A Customer \n\t0 ---- Logout\n[CHOICE]: '))
        if choice == 1:
            self.search()
        elif choice == 2:
            self.create()
            self.cust_menu()
        elif choice == 3:
            self.update()
        elif choice == 4:
            self.delete()
        elif choice == 0:
            logout()
        
    def create(self):
        ss_number = input('[SOCIAL SECURITY NUMBER]: ')
        first_name = input('[FIRST NAME]: ')
        last_name = input('[LAST NAME]: ')
        email_address = input('[EMAIL ADDRESS]: ')
        phone_number = input('[PHONE NUMBER]: ')
        physical_address = input('[PHYSICAL ADDRESS]: ')
        username = input('Temp username [CUSTOMER CREATES THEIR OWN!]: ')
        password = input('Temp password [CUSTOMER CREATES THEIR OWN!]: ')
        self.set_values(ss_number, first_name, last_name, email_address, phone_number, physical_address, username, password)
        self.insertDataIntoDB()
        self.go_home()

    def insertDataIntoDB(self):
        try:
            data = [(self.ss_number, self.first_name, self.last_name, self.email_address, self.phone_number, self.physical_address, self.username, self.password)]
            sql = "INSERT INTO customer (ss_number, first_name, last_name, email_address, phone_number, physical_address, username, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            cur.executemany(sql, data)
            conn.commit()
            print("CUSTOMER CREATED!")
        except Exception as ex:
            print(ex)

    def search(self):
        ss_number = input('\nType in ss_number: ')
        self.fetchData(ss_number)
        print('Done!')
        
    def fetchData(self, ss_number):
        try:
            sql = f'SELECT * FROM customer WHERE ss_number="{ss_number}"'
            result = cur.execute(sql).fetchall()
            if not result:
                print('Wrong ss_Number!')
                self.search()
            else:
                for row in result:                
                    ss_number, first_name, last_name, email_address, phone_number, physical_address, username, password = row
                    print(f'\n[CUSTOMER DETAILS]:\n{line}\nSS_Number: {ss_number}\nFirst Name: {first_name}\nLast Name: {last_name}\nEmail Address: {email_address}\nPhone Number: {phone_number}\nPhysical Address: {physical_address}')
                    self.go_home()
        except Exception as ex:
            print(ex)

    def update(self):
        customer_ssn = input('\nType in customer ssn to update: ')
        sql = f"SELECT ss_number, first_name, last_name, email_address, phone_number, physical_address FROM customer WHERE ss_number='{customer_ssn}'"
        result = cur.execute(sql).fetchall()
        if not result:
            print('[ERROR]: Wrong SSN!')
            self.go_home()
        else:
            for row in result:
                [ss_number, first_name, last_name, email_address, phone_number, physical_address] = row 
                for i in row:
                    check_value = input(f'Edit ({i}) or [RETURN]: ')
                    if not check_value:
                        check_value = i
                    stack.put(check_value)
            self.add_updates(customer_ssn)
            self.go_home()

    def add_updates(self, customer_ssn):
        sql = f"UPDATE customer set physical_address='{stack.get(True)}', phone_number='{stack.get(True)}', email_address='{stack.get(True)}', last_name='{stack.get(True)}', first_name='{stack.get(True)}', ss_number='{stack.get(True)}'  WHERE ss_number='{customer_ssn}'"
        cur.execute(sql)
        conn.commit()
        print('[CUSTOMER UPDATED!]')

    def delete(self):
        customer_ssn = input('[SOCIAL SECURITY NUMBER]: ')
        sql = f"DELETE FROM customer WHERE ss_number='{customer_ssn}'"
        cur.execute(sql)
        conn.commit()
        print(f'[CUSTOMER REMOVED!]')
        self.go_home()

    def go_home(self):
        main_m = input(f"{line}\n[MAIN MENU]: yes or no? ")
        if main_m.lower() == 'yes':
            self.cust_menu()
        else:
            print('[PLEASE CALL AGAIN!]')
            quit(0)
