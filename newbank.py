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
====================================================================================================================================
#Notifications
from datetime import datetime
def check_credit_payment(username):
    user_data = bankfile[bankfile['username'] == username]
    credit_amount = user_data['Credit Amount'].values[0]
    
    # Get today's date
    today = datetime.now()
    
    # Check if it's past the 25th of the month
    if today.day >= 25:
        # Payment due on the 25th of next month
        next_payment_date = datetime(today.year, today.month + 1, 25)
    else:
        # Payment due on the 25th of this month
        next_payment_date = datetime(today.year, today.month, 25)
    
    # Calculate days until next payment
    days_until_payment = (next_payment_date - today).days
    
    if days_until_payment == 0:
        print(f"Payment for credit amount ${credit_amount} is due today!")
    else:
        print(f"Your next credit payment of ${credit_amount} is due in {days_until_payment} days.")

===========================================================================================================================================
#Appointments

# Initialize a dictionary to store appointments
appointment_schedule = {}

def schedule_appointment(username):
    appointment_times = {
        '9AM': 'yes',
        '11AM': 'no',
        '1PM': 'yes',
        '3PM': 'no'
    }

    print("Available appointment times:")
    for time, status in appointment_times.items():
        if status == 'yes':
            print(time)

    chosen_time = input("Please enter your desired appointment time: ").upper()

    if chosen_time in appointment_times and appointment_times[chosen_time] == 'yes':
        print("Appointment scheduled!")
        appointment_schedule[username] = chosen_time  # Store the appointment in the dictionary
    else:
        print("Sorry, appointment time is not available.")


===============================================================================================================================
#Balance enquiry
def balance_enquiry(username):
    user_data = bankfile[bankfile['username'] == username]
    print("Select an account type:")
    print("1. Checking")
    print("2. Savings")
    account_choice = input("Please enter your choice (1 or 2): ")
    
    if account_choice == '1':
        checking_balance = user_data['checking($)'].values[0]
        print(f"Checking account balance for {username}: ${checking_balance}")
    elif account_choice == '2':
        savings_balance = user_data['saving($)'].values[0]
        print(f"Savings account balance for {username}: ${savings_balance}")
    else:
        print("Invalid choice.")
