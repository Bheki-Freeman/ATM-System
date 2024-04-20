import employee
import customer
import account
import sqlite3
from getpass import getpass
from datetime import date 

line = '*' * 41
conn = sqlite3.connect('main.db')
cur = conn.cursor()
today = date.today()


class Admin(employee.Employee):
    session_name = None
    acc = account.Account()

    def login(self):
        super()
        username = input('{}\nUsername: '.format(line))
        password = getpass('Password: ')
        if self.fetchData(username, password):
            self.mainMenu()
        else:
            print("[ERROR]: Wrong User!")
            self.login()
    
    def acc_menu(self):
        print(f'{line}\n** ACCOUNTS DASH-BOARD **\n{line}\n')
        action = int(input('What are we doing?\n1 ---- Find Account\n2 ---- List Accounts\n3 ---- Create Account\n4 ---- Update Customer Accounts\n5 ---- Delete Customer Account\n\t[CHOICE]: '))
        if action == 1:
            self.acc.find_account()
        elif action == 2:
            self.acc.list_accounts()
        elif action == 3:
            self.acc.create_account()
        elif action == 4:
            self.acc.update_account()
        elif action == 5:
            self.acc.delete_account()
        else:
            print(f'[ERROR]: Wrong input!')
            self.acc_menu()


    def fetchData(self, username, password):
        global session_name
        sql = f'SELECT first_name, username, password FROM admin WHERE username="{username}" AND password="{password}"'
        result = cur.execute(sql).fetchall()
        if not result:
            return False
        else:
            for row in result:                
                first_name, username, password = row
                session_name = first_name
            return True
    
    def mainMenu(self):
        print(f'\n **** WELCOME ADMINISTRATOR ****')
        print(f'\n{line}\n[DATE]: {today}  [ADMIN]: {session_name}\n{line}\n')
        choice = int(input((f'\n\t1 ---- Customers Menu\n\t2 ---- Employees Menu\n\t3 ---- Accounts\n[CHOICE]: ')))
        if choice == 1:
            cust = customer.Customer()
            cust.cust_menu()
        elif choice == 2:
            self.emp_menu()
        elif choice == 3:
            self.acc_menu()
        else :
            print('[ERROR]: Wrong input!')

    def emp_menu(self):        
        print(f'{line}\n\t [EMPLOYEE DASH-BOARD]\n{line}\n')
        choice = int(input('What are we doing Today:\n\t1 ---- Find Staff Member By Job ID\n\t2 ---- Add New Staff Member\n\t3 ---- Update Staff Details'+
                           '\n\t4 ---- Delete A Staff Member\n\t0 ---- Home\n[CHOICE]: '))
        if choice == 1:
            self.search()
        elif choice == 2:
            self.register()
            self.emp_menu()
        elif choice == 3:
            self.update()
        elif choice == 4:
            self.delete()
        elif choice == 0:
            self.mainMenu()
        else:
            print('[ERROR]: Wrong Choice!')
            self.emp_menu()
