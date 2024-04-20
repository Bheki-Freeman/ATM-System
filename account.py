import queue
from re import split
from shlex import join
from random import randint
import sqlite3
from datetime import date


conn = sqlite3.connect('main.db')
cur  = conn.cursor()
today = date.today()
line = '*' * 41
q_v = queue.LifoQueue()

class Account():
    acc_names = ['sicalo', 'savings', 'gold']
    balance = 0
    acc_name = ''
    acc_number = 00
    customer_ssn = 0
    
    def __init__(self) -> None:
        pass
    def check_balance(self):
        return self.balance

    def set_values(self, acc_name, acc_number, customer_ssn, date_created, balance):
        self.acc_name = acc_name
        self.acc_number = acc_number
        self.customer_ssn = customer_ssn
        self.date_created = date_created
        self.balance = balance

    def find_account(self):
        acc_number = int(input('[ACCOUNT NUMBER]: '))
        sql = f"SELECT * FROM accounts WHERE acc_number='{acc_number}'"
        result = cur.execute(sql).fetchall()
        if not result:
            print('[ERROR]: Account not Found!')
            self.find_account()
        else:
            for row in result:
                [acc_number, acc_name, customer_ssn, date_created, balance] = row
                print('[ACCOUNT DETAILS]:')
                print('{:<10s} {:<10s} {:<10s} {:<15s} {:<10s}'.format('Acc Number', 'Acc Name', 'Cust SSN', 'Date Created', 'Balance'))
                print('{:<10d} {:<10s} {:<10s} {:<15s} {:<10s}'.format(acc_number, acc_name, customer_ssn, date_created, balance))

    def list_accounts(self):
        sql = f"SELECT * FROM accounts"
        result = cur.execute(sql).fetchall()
        print(f'{line}\n[ACCOUNT DETAILS]:\n{line}\n')
        print('{:<10s} {:<10s} {:<10s} {:<15s} {:<10s}'.format('Acc Number', 'Acc Name', 'Cust SSN', 'Date Created', 'Balance'))
        for row in result:
                [acc_number, acc_name, customer_ssn, date_created, balance] = row
                print('{:<10d} {:<10s} {:<10s} {:<15s} {:<10s}'.format(acc_number, acc_name, customer_ssn, date_created, balance))

    def update_account(self):
        acc_number = int(input('[ACCOUNT NUMBER]: '))
        sql = f"SELECT * FROM accounts WHERE acc_number='{acc_number}'"
        result = cur.execute(sql).fetchall()
        if not result:
            print('[ERROR]: Account not Found!')
            self.update_account()
        else:
            for row in result:
                [acc_number, acc_name, customer_ssn, date_created, balance] = row
                for i in row:
                    check_value = input(f'Edit ({i}) or [RETURN]: ')
                    if not check_value:
                        check_value = i
                    q_v.put(check_value)
            self.add_updates(acc_number)
        pass
    
    def add_updates(self, acc_number):
        sql = f"UPDATE accounts set balance='{q_v.get(True)}', date_created='{q_v.get(True)}', customer_ssn='{q_v.get(True)}', acc_name='{q_v.get(True)}', acc_number='{q_v.get(True)}'  WHERE acc_number='{acc_number}'"
        cur.execute(sql)
        conn.commit()
        print('[ACCOUNT UPDATED!]')

    def delete_account(self):
        acc_number = int(input('[ACCOUNT NUMBER]: '))
        sql = f"SELECT * FROM accounts WHERE acc_number='{acc_number}'"
        result = cur.execute(sql).fetchall()
        if not result:
            print('[ERROR]: Account not Found!')
            self.delete_account()
        else:
            sql = f"DELETE FROM accounts WHERE acc_number ='{acc_number}'"
            cur.execute(sql)
            conn.commit()
            print('[ACCOUNT REMOVED!]')
        
    def add_account(self):
        sql = f"INSERT INTO accounts values('{self.acc_number}', '{self.acc_name}',  '{self.customer_ssn}', '{self.date_created}', '{self.balance}')"
        cur.execute(sql)
        conn.commit()


    def create_account(self):
        ran_num = randint(90000000, 999999999)        
        acc_name = input(f'[ACCOUNT NAME]: ({" ".join(self.acc_names)}) : ')
        customer_ssn = input('[CUSTOMER SSN]: ')
        date_created = today
        if self.verify_account(ran_num):
            ran_num = randint(90000000, 999999999)
        else:
            acc_number = ran_num
        user_details = input(f'{line}\n\t[ACCOUNT DETAILS]:\n{line}\nAccount Name: {acc_name}\nAccount Number: {acc_number}\nCustomer SSN: {customer_ssn}\nDate: {date_created}\nBalance: {self.balance}\n\nVerify Details [yes or edit]: ')
        if user_details.lower() == 'yes':
            self.set_values(acc_name, acc_number, customer_ssn, date_created, self.balance)
            self.add_account()
            print(f'{line}\n[ACCOUNT CREATED!]\n{line}\n')
            go_menu = input('[ADD ANOTHER?] (yes / no): ')
            if go_menu.lower() == 'yes':
                self.create_account()
            else:
                print('[PLEASE CALL AGAIN!]')
                quit(0)
        else:
            self.create_account()  
        
    def verify_account(self, acc_number):
        sql = f"SELECT acc_number from accounts WHERE acc_number='{acc_number}'"
        result = cur.execute(sql).fetchall()
        if not result:
            return False
        else:
            return True
    
    def make_transfere(self):
        reciever_account = int(input('Type in the recieving account: '))
        amount = float(input('[TRANSFER AMOUNT]: '))
        temp_withdrawal = self.make_withdrawal(amount)
        q_v.put(temp_withdrawal) # We need to verify if account is reachable, before sending money to it
        if self.verify_account(reciever_account):
            sql = f"SELECT acc_name, balance from accounts WHERE acc_number='{reciever_account}'"
            bal = cur.execute(sql).fetchall()
            for row in bal:
                [acc_name, balance] = row
                new_bal = (float(balance) + amount)
                sql = f'UPDATE accounts SET balance="{new_bal}" WHERE acc_number="{reciever_account}"'
                cur.execute(sql)
                conn.commit()
                print('[TRANSFER SUCCESSFUL!]')
        else:
            print('Account Not verified!')
        
    def make_deposit(self):
        amount = float(input('[DEPOSIT AMOUNT]: '))
        balance = float(self.balance) + amount
        self.balance = balance
        sql = f'UPDATE accounts SET balance="{self.balance}" WHERE customer_ssn="{self.customer_ssn}"'
        cur.execute(sql)
        conn.commit()
        print('[DEPOSIT SUCCESSFUL!]')
    def make_withdrawal(self, amount):
        if float(self.balance) >= amount:
            balance = float(self.balance) - amount
            self.balance = balance
            sql = f"UPDATE accounts SET balance='{self.balance}' WHERE customer_ssn='{self.customer_ssn}'"
            cur.execute(sql)
            conn.commit()
            print('Withdrawal Accepted!')
        else:
            print('[LOW FUNDS]: account is too low for the withdrawal!')
            dep = input('Want to make Deposit? yes or no: ')
            if dep == 'yes':
                self.make_deposit()
                print(f'Available Balance: {self.check_balance()}')
            else:
                return
        return self.balance


