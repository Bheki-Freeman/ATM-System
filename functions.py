from atm import splashScreen

line = '*' * 41

def logout():
    print(f'{line}\n**** THANK YOU FOR PATRONIZING US ! ****\n{line}')
    login = int(input('\n1 ----  [LOGIN] \t0 ---- [EXIT] \n[CHOICE]: '))
    if login == 1:
        splashScreen()
    elif login == 0:
        print('PLEASE CALL AGAIN!')
        exit()

