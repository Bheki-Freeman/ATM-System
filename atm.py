import admin
from account import Account
from datetime import datetime, date 
from getpass import getpass
import sqlite3

conn = sqlite3.connect('main.db')
cur = conn.cursor()

line = '*' * 41
today = date.today()
n_w = datetime.now()
current_time = f'{n_w.hour} : {n_w.minute} : {n_w.second}'

class ATM(object):
    acc = Account()
    def __init__(self) -> None:
        pass
    def quit_s(self):
        print('PLEASE CALL AGAIN!')
        exit()

    def fetchAccountDetails(self, ss_number):
        try:
            sql = f'SELECT * FROM accounts WHERE customer_ssn="{ss_number}"'
            result = cur.execute(sql).fetchall()
            if not result:
                 print('Wrong ss_Number!')
                 home = input('[HOME?]: (yes / no) ')
                 if home.lower() == 'yes':
                    self.customer_menu()
                 else:
                     self.quit_s()
            else:
                for row in result:                
                    acc_number, acc_name, customer_ssn, date, balance = row
                    self.acc.set_values(acc_name, acc_number, customer_ssn, date, balance) 
        except Exception as ex:
           print(ex)

    def customer_menu(self):        
        self.fetchAccountDetails(session_name)
        print(f'{line}\n\t[WELCOME TO OUR BANK] ({session_name})\n{line}')
        actions = int(input("What are we Doing Today? \n1 ---- Check Balances\n2 ---- Make Deposits\n3 ---- Make Withdrawals\n4 ---- Transfers\n0 ---- Logout\n\n[CHOICE]: "))
        if actions == 1:
            self.display_balance()
            self.go_home()
        elif actions == 2:
            self.acc.make_deposit()
            self.go_home()
        elif actions == 3:
            amount = float(input('[WITHDRAWAL AMOUNT]: '))
            self.acc.make_withdrawal(amount=amount)
            self.go_home()
        elif actions == 4:
            self.acc.make_transfere()
            self.go_home()
        elif actions == 0:
            print('[PLEASE CALL AGAIN!]')
            exit(0)
        else:
            print('[ERROR]: Wrong input!')
            self.go_home()

    def display_balance(self):
        print(f'{line}\n\t[ACCOUNT BALANCES]\n{line}\n')
        print('{:>6s} {:>12s} {:>10s} {:>10s} {:>10s}'.format('Account', 'Acc Number', 'SS Number', 'Balance', 'Av. Balance'))
        print('{:>6s} {:>12d} {:>10s} {:>10.2f} {:>10.2f}'.format(self.acc.acc_name, self.acc.acc_number, self.acc.customer_ssn, float(self.acc.balance), float(self.acc.balance)-100))

    def go_home(self):
        home = input('\n[HOME?] yes or no ')
        if home.lower() == 'yes':
            self.customer_menu()
        else:
            self.quit_s()

    def fetchData(self, username, password):
        global session_name
        sql = f'SELECT ss_number, first_name, username, password FROM customer WHERE username="{username}" AND password="{password}"'
        result = cur.execute(sql).fetchall()
        if not result:
            return False
        else:
            for row in result:                
                ss_number, first_name, username, password = row
                session_name = ss_number
            return True
    
    def customerLogin(self):
        username = input('{}\nUsername: '.format(line))
        password = getpass('Password: ')
        if self.fetchData(username, password):
            self.customer_menu()
        else:
            print("[ERROR]: Wrong User!")
            self.customerLogin()
    def administratorLogin(self):
        admin.Admin().login()

atm = ATM()




def splashScreen():
        print(f'\n* [DTE]: {today} [TME]: {current_time} *')
        print(f'{line}\n\tWELCOME INTO OUR ATM SYSTEM\n{line}\n')
        
        login_type = int(input((f'\n\tLogin Type: \n\t\t1 ---- Customer\n\t\t3 ---- Administrator\n[CHOICE]: ')))
        
        try :
            if login_type == 1:
                atm.customerLogin()            
            elif login_type == 3:
                atm.administratorLogin()
            else :
                print(f'[ERROR]: Wrong Input: {login_type}')
        except ValueError as ex:
                print(ex)

if __name__=='__main__':
    splashScreen()