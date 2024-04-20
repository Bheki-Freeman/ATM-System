from random import randint
import random
from getpass import getpass
import sqlite3


# Globals
conn = sqlite3.connect('main.db')
cur = conn.cursor()
line = '*' * 41

class Employee(object):
    def __init__(self):
        pass

    def search(self):
        print('Searching ...')
    def update(self):
        print('Wait a minute, Updating ...')
    def delete(self):
        print('Okay, let us delete this one..')

    def set_values(self, first_name, last_name, job_id, job_title, n_id, user_name, password) -> None:
        self.first_name = first_name
        self.last_name =  last_name
        self.job_id = job_id
        self.job_title = job_title
        self.n_id = n_id
        self.user_name = user_name
        self.password = password

    def register(self):
        bank_dptmts = ['BSM', 'BCM', 'BCC', 'BST']
        f_name = input('Enter Emp First Name: ')
        l_name = input('Enter Emp Last Name: ')
        job_id = f'{random.choice(bank_dptmts)}{randint(1001, 5009)}'
        job_title = input('Enter Emp job Title: ')
        n_id = (int(input('Enter Emp national Id: ')))
        user_name = input('Create Emp username: ')
        password = getpass('Create Emp Password: ') 
        self.set_values(f_name, l_name, job_id, job_title, n_id, user_name, password)
        self.insertDataIntoDB()

    def printValues(self):
        values = f'Your values : \n\t   {self.first_name} {self.last_name} {self.job_id} {self.job_title} {self.n_id} {self.user_name} {self.password}'
        print(values)

    def login(self):
        pass
    
    def insertDataIntoDB(self):
        sql = None
        try:
            data = [(self.job_id, self.first_name, self.last_name, self.job_title, self.n_id, self.user_name, self.password)]
            if self.job_title.lower() == 'administrator' or self.job_title.lower() == 'admin':
                sql = "INSERT INTO admin (job_id, first_name, last_name, job_title, n_id, username, password) VALUES (?, ?, ?, ?, ?, ?, ?)"
            else:
                sql = "INSERT INTO employee (job_id, first_name, last_name, job_title, n_id, username, password) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cur.executemany(sql, data)
            conn.commit()
            print("EMPLOYEE CREATED!")
        except Exception as ex:
            print(ex)
