import sys
import pandas as pd
file_path = r"Python_BankData.csv"
bankfile = pd.read_csv(file_path)

# Account Access
def verify_credentials(username, password, bankfile):
    return str(bankfile.loc[bankfile['username'] == username, 'password'].values[0]) == password
def verify_credentials_code(username, third_platform_code, bankfile):
    return str(bankfile.loc[bankfile['username'] == username, 'third_platform_code'].values[0]) == third_platform_code

def displayMenu():
    print("1. Money Transfer")
    print("2. Bill Payment")
    print("3. Appointment")
    print("4. Notification")
    print("5. Loans")
    print("6. Exit")
    choice = input("Enter your choice: ")
    return choice

def Accountaccess():
    attempts = 0
    tp_attempt = 0
    username = input("Enter your username: ")
    
    if username in bankfile['username'].values:
        while attempts < 3:
            password = input("Enter your password: ")
            
            if verify_credentials(username, password, bankfile):
                while tp_attempt < 3:
                    third_platform_code = input("Enter the third-platform code: ")
                    
                    if verify_credentials_code(username, third_platform_code, bankfile):
                        print(f"Hi {username}, Welcome!")
                        
                        while True:  # Loop to keep displaying the menu until the user exits
                            choice = displayMenu()
                            
                            if choice == '1':
                                moneytransfer(username)
                            elif choice == '2':
                                bill_payment(username)
                            elif choice == '3':
                                schedule_appointment(username)
                            elif choice == '4':
                                pass  # Add logic for notifications
                            elif choice == '5':
                                accountnumber = int(input('Please enter your account number: '))
                                loanapply(accountnumber)
                            elif choice == '6':
                                sys.exit('Thank you')
                            else:
                                print("Invalid choice.")
                    else:
                        tp_attempt += 1
                        print("Third-platform code incorrect.")
                        if tp_attempt == 3:
                            print("Third-platform code verification failed.")
            else:
                print("Incorrect password.")
                attempts += 1
    else:
        print("Incorrect username.")
        if attempts == 3:
            print("Your account is blocked. Please go to the nearest bank branch to ask for help.")

def main():
    Accountaccess()

if __name__ == "__main__":
    main()

# 1. Money Transfer
def moneytransfer(username):
    user_choice = int(input('Internal transfer or external transfer(1/2):'))
    if user_choice == 1:
        saving = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0]
        checking = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
        print(f'saving balance:{saving:.2f}')
        print(f'checking balance:{checking:.2f}')
        print('1.Checking to Saving.')
        print('2.Saving to Checking.')
        s_or_ch=input('Enter your choice:')
        if(s_or_ch=="1"):
            amount1 = float(input('How much money would you like to transfer:'))
            if amount1 <= checking:
                print('transfer successfully')
                new_checking = checking - amount1
                bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0] = new_checking
                new_saving = saving + amount1
                bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0] = new_saving
                print(f'New saving :{new_saving:.2f}')
                print(f'New checking :{new_checking:.2f}')
        elif(s_or_ch=="2"):
            amount1 = float(input('How much money would you like to transfer:'))
            if amount1 <= saving:
                print('transfer successfully')
                new_saving = saving - amount1
                bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0] = new_saving
                new_checking = checking + amount1
                bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0] = new_checking
                print(f'New saving :{new_saving:.2f}')
                print(f'New checking :{new_checking:.2f}')
        else:
            print("Wrong command!")
    if user_choice == 2:
        checking = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
        print(f'saving balance:{checking:6}')
        external_account = input('Input the account number you want to transfer to:')
        amount2 = float(input('Input the amount you want to send:'))
        if amount2 > checking:
            print("Insuffient amount!")
        elif amount2 <= checking and amount2 <= 2000:
            new_checking = checking - amount2
            bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0] = new_checking
            print(f'New checking :{new_checking:.2f}')
            print('transfer successfully')
            # print(bankfile.loc[bankfile['username'] == username, 'saving($)'])
        elif amount2 > 2000:   # if the amount is larger than the banchmark
            print('your pin number is sent')
            pin = int(input('please input your pin number:'))
            if pin == 000:  # here the pin suppose to be the one random number and we just let the user use 000 as the pin in
                new_checking = checking - amount2
                bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0] = new_checking
                print(f'New checking :{new_checking:.2f}')
                print('transfer successfully')
