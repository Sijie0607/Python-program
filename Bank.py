import pandas as pd
file_path = r"C:\Users\ellac\OneDrive\Desktop\Python_BankData.csv"
bankfile = pd.read_csv(file_path)


def bill_payment(username):
    

    user_data = bankfile[bankfile['username'] == username]

    if user_data.empty:
        print("User not found.")
        return

    print("Bill payment option selected.")
    print("Select an option:")
    print("1. Pay bill")
    print("2. View bill payment history")
    sub_option = input("Enter your choice (1 or 2): ")

    if sub_option == '1':
        print("Select a bill type:")
        print("1. Electricity")
        print("2. Water")
        print("3. Gas")
        bill_type_choice = input("Enter your choice (1 to 3): ")

        bill_types = ['electricity', 'water', 'gas']
        bill_type = bill_types[int(bill_type_choice) - 1]

        amount_to_pay = float(input(f"Enter the amount to pay for {bill_type}: "))

        initial_balance = user_data.loc[:, 'checking($)'].values[0]
        print(f"Initial balance in checking account: ${initial_balance}")

        confirmation = input(f"Confirm payment of ${amount_to_pay} for {bill_type}. Enter 'yes' to confirm: ")

        if confirmation.lower() == 'yes':

           bankfile.loc[bankfile['username'] == username, 'checking($)'] -= amount_to_pay
           updated_balance = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
           print(f"Payment of ${amount_to_pay} for {bill_type} successful.")
           print(f"Updated balance in checking account: ${updated_balance}")
           bankfile[bankfile['username'] == username] = user_data
           bankfile.to_csv(r"C:\Users\ellac\OneDrive\Desktop\Python_BankData.csv", index=False)
        else:
            print("Payment cancelled.")

    elif sub_option == '2':
        print(user_data.loc[:, 'bill history'].values[0])

    else:
        print("Invalid choice.")


def moneytransfer(username):
    user_choice = int(input('Internal transfer or external transfer(1/2):'))
    if user_choice == 1:
        saving = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0]
        print(f'saving balance:{saving:6}')
        amount1 = float(input('How much money would you like to transfer:'))
        if amount1 <= saving:
            print('transfer successfully')
            new_saving = saving - amount1
            bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0] = new_saving
            checking = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
            new_checking = checking - amount1
            bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0] = new_checking
            print(f'new_saving ={new_saving:6}')
            print(f'new_checking ={new_checking:6}')
            print(bankfile.loc[bankfile['username'] == username, 'saving($)', 'checking($)'])
    if user_choice == 2:
        saving = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0]
        print(f'saving balance:{saving:6}')
        external_account = input('input the account number you want to transfer to:')
        amount2 = float(input('Input the amount you want to send:'))
        if amount2 <= saving and amount2 <= 2000:
            new_saving = saving - amount2
            index = bankfile.loc[bankfile['username'] == username, 'saving($)'].index[0]  # after the sorting on username row and saving($)column, there is only one value in this series
            bankfile.at[index, 'saving($)'] = new_saving
            print(bankfile['saving($)'])
            print(bankfile.loc[bankfile['username'] == username, 'saving($)'])
            print('transfer successfully')
            # print(bankfile.loc[bankfile['username'] == username, 'saving($)'])
        elif amount2 > 2000:   # if the amount is larger than the banchmark
            print('your pin number is sent')
            pin = float(input('please input your pin number:'))
            if pin == 000:  # here the pin suppose to be the one random number and we just let the user use 000 as the pin in
                bankfile.loc[bankfile['username'] == username, 'saving($)'] = bankfile.loc[bankfile['username'] == username, 'saving($)'] - amount2
                print('transfer successfully')
                print(bankfile['saving($)'])

def loanapply(accountnumber):
    accountnumber = input('please input your account number:')
    if accountnumber in bankfile['account_number'].values:
        credit_score = bankfile.loc[bankfile['account_number'] == accountnumber, 'credit_score'].values[0]
        print(f'Your credit score is: {credit_score}')
        loan_amount = float(input('Enter the loan amount you need:'))
        saving_amount = bankfile.loc[bankfile['account_number'] == accountnumber, 'saving($)'].values[0]
        loan_to_saving_ratio = loan_amount / saving_amount
        print(f'Loan to Saving Ratio: {loan_to_saving_ratio:.2%}')
    else:
        print('Nonexistent Account')

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

    chosen_time = input("Enter your desired appointment time: ")

    if chosen_time in appointment_times and appointment_times[chosen_time] == 'yes':
        print("Appointment scheduled!")
        appointment_schedule[username] = chosen_time  # Store the appointment in the dictionary
    else:
        print("Sorry, appointment time is not available.")


        chosen_time = input("Enter your desired appointment time: ")

        if chosen_time in appointment_times and appointment_times[chosen_time] == 'yes':
            print("Appointment scheduled!")
            schedule_appointment[username] = chosen_time
        else:
            print("Sorry, appointment time is not available.")

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
                                print('Thank you')
                                break  # Exit the menu loop and end the program
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
==================================================================================================================================







































import csv
import sys
import pandas as pd

# Function to verify user credentials
def verify_credentials(username, password, bankfile):
    return str(bankfile.loc[bankfile['username'] == username, 'password'].values[0]) == password
def verify_credentials_code(username, third_platform_code, bankfile):
    return str(bankfile.loc[bankfile['username'] == username, 'third_platform_code'].values[0]) == third_platform_code

def displayMenu():
    print("1. Account Access")
    print("2. Bill Payment")
    print("3. Appointment")
    print("4. Notification")
    print("5. Loans")
    print("6. Exit")
    choice=input("Enter your choice: ")
    return choice
# Main function
def main():
    file_path = "Python_BankData.csv"
    bankfile = pd.read_csv(file_path)
    attempts = 0
    tp_attempt = 0

    while attempts < 3:     # username can be tried innfinite times, but password can only be tried 3 times. after thhat, the account will be blocked
        username = input("Enter your username: ")
        if username in bankfile['username'].values:
            while(attempts < 3):
                password = input("Enter your password: ")
                if verify_credentials(username, password, bankfile):
                    while tp_attempt < 3:
                        third_platform_code = input("Enter the third-platform code: ")      #Since we are unable to write code in another platform to send the third-platform code, 
                        if verify_credentials_code(username, third_platform_code, bankfile):       
                            print(f"Hi {username}, Welcome!")
                            choice=displayMenu()
                            return  
                        else:
                            tp_attempt += 1
                            print("Third-platform code incorrect.")
                            if tp_attempt == 3:
                                print("Third-platform code verification failed.")
                                return
                else:
                    print("Incorrect password.")
                    attempts += 1
        else:
            print("Incorrect username.")

    if attempts == 3:
        print("Your account is blocked. Please go to the nearest bank branch to ask for help.")

if __name__ == "__main__":
    main()
#*********************************************************************
data = []  # Initialize an empty list to hold the data

# Open the CSV file and read the data into a list of dictionaries
with open(r"C:\Users\ellac\OneDrive\Desktop\Python\Python_BankData.csv", newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

# Verification code dictionary (username as key, code as value)
verification_codes = {
    'Abby': 'abc123',
    'Bella': 'def456',
    'Cathy': 'ghi789',
    'Dora': 'jkl012',
    'Emma': 'mno345'
}

=====================================================================================================================================================
##Appointment Function
def schedule_appointment(option, user_id):
    if option == 3:
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

        chosen_time = input("Enter your desired appointment time: ")

        if chosen_time in appointment_times and appointment_times[chosen_time] == 'yes':
            print("Appointment scheduled!")
            appointment_schedule[user_id] = chosen_time
        else:
            print("Sorry, appointment time is not available.")

================================================================================================================================
## Bill Payment Function
def process_bill_payment(option, user_id):
    if option == 2:
        print("Select a bill type:")
        print("1. Water")
        print("2. Electricity")
        bill_type = int(input("Enter your choice (1 or 2): "))
        if bill_type == 1:
            amount = float(input("Enter the amount to pay for water bill: "))
            result = bill_payment(user_id, 'water', amount)
            print(result)
        elif bill_type == 2:
            amount = float(input("Enter the amount to pay for electricity bill: "))
            result = bill_payment(user_id, 'electricity', amount)
            print(result)
        else:
            print("Invalid choice")





===========================================================================================================
import csv
import sys

# Function to verify user credentials
def verify_credentials(username, password, user_data):    #user_data: dictory
    return user_data.get(username) == password         ##.get: username is key and password 是返回的值，如果username和password对应，true；反之则false

# Load user data from CSV 
def load_user_data(csv_file_path):
    user_data = {} ##

    # Read CSV and process data
    with open(csv_file_path, mode = 'r') as file:     
        csv_reader = csv.DictReader(file)
        for row in csv_reader: # try column
            username = row["username"]
            password = row["password"]
            # Store the username as key and password as value in the dictionary
            user_data[username] = password
    return user_data
def displayMenu():
    print("1.Balance Enquiry")
    print("1. Money Transfer")
    print("2. Bill Payment")
    print("3. Appointment")
    print("4. Notification")
    print("5. Loans")
    print("6. Exit")
    choice=input("Enter your choice: ")
    return choice
# Main function
def main():
    user_data = load_user_data("Python_BankData.csv")  
    attempts = 0
    tp_attempt = 0

    while attempts < 3:     # username can be tried innfinite times, but password can only be tried 3 times. after thhat, the account will be blocked
        username = input("Enter your username: ")
        if username in user_data:
            while(attempts < 3):
                password = input("Enter your password: ")
                if verify_credentials(username, password, user_data):
                    while tp_attempt < 3:
                        third_platform_code = input("Enter the third-platform code: ")      #Since we are unable to write code in another platform to send the third-platform code, 
                        if third_platform_code == "996":        # we just assume the code is 996 here.
                            print(f"Hi {username}, Welcome!")
                            choice=displayMenu()
                            return  
                        else:
                            tp_attempt += 1
                            if tp_attempt == 3:
                                print("Third-platform code verification failed.")
                                return
                else:
                    print("Incorrect password.")
                    attempts += 1
        else:
            print("Incorrect username.")

    if attempts == 3:
        print("Your account is blocked. Please go to the nearest bank branch to ask for help.")

if __name__ == "__main__":
    main()
===========================================================================================
import pandas as pd
file_path = "C:\\Users\\hw\\Desktop\\python\\Python_BankData.csv"
bankfile = pd.read_csv(file_path)
print(bankfile)
external_account = []


def moneytransfer(username): ## accountaccess
    user_choice = int(input('Internal transfer or external transfer(1/2):'))
    if user_choice == 1: ## add the choice for customer to have a choice of their account
        saving = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0]
        print(f'saving balance:{saving:6}')
        amount_internal = float(input('How much money would you like to transfer:'))  #amount1)
        if amount1 <= saving:
            print('transfer successfully')
            new_saving = saving - amount1
            bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0] = new_saving
            checking = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0] ##checking account also can transfer money
            new_checking = checking - amount1
            bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0] = new_checking
            print(f'new_saving ={new_saving:6}')
            print(f'new_checking ={new_checking:6}')
            print(bankfile.loc[bankfile['username'] == username, 'saving($)', 'checking($)'])
    if user_choice == 2:  ## choose your saving or checking account
        saving = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0]
        print(f'saving balance:{saving:6}')
        external_account = input('input the account number you want to transfer to:')
        amount_external = float(input('Input the amount you want to send:'))
        if amount2 <= saving and amount2 <= 2000:
            new_saving = saving - amount2
            index = bankfile.loc[bankfile['username'] == username, 'saving($)'].index[0]  # after the sorting on username row and saving($)column, there is only one value in this series
            bankfile.at[index, 'saving($)'] = new_saving
            print(bankfile['saving($)'])
            print(bankfile.loc[bankfile['username'] == username, 'saving($)'])
            print('transfer successfully')
            # print(bankfile.loc[bankfile['username'] == username, 'saving($)'])
        elif amount2 > 2000:   # if the amount is larger than the banchmark
            print('your pin number is sent')
            pin = float(input('please input your pin number:'))
            if pin == 000:  # here the pin suppose to be the one random number and we just let the user use 000 as the pin in
                bankfile.loc[bankfile['username'] == username, 'saving($)'] = bankfile.loc[bankfile['username'] == username, 'saving($)'] - amount2
                print('transfer successfully')
                print(bankfile['saving($)'])


username = input('your username')
moneytransfer(username)

def loanapply(accountnumber):
    accountnumber = input('please input your account number:')
    if input_account_number in bankfile['account_number'].values:
        credit_score = bankfile.loc[bankfile['account_number'] == input_account_number, 'credit_score'].values[0]
        print(f'Your credit score is: {credit_score}')
        loan_amount = float(input('Enter the loan amount you need:'))
        saving_amount = bankfile.loc[bankfile['account_number'] == input_account_number, 'saving($)'].values[0]
        loan_to_saving_ratio = loan_amount / saving_amount
        print(f'Loan to Saving Ratio: {loan_to_saving_ratio:.2%}')
    else:
        print('Nonexistent Account')



==========================================================================================================================
elif option == 2:
                            print("Select a bill type:")
                            print("1. Water")
                            print("2. Electricity")
                            bill_type = int(input("Enter your choice (1 or 2): "))
                            if bill_type == 1:
                                amount = float(input("Enter the amount to pay for water bill: "))
                                result = bill_payment(user_id, 'water', amount)
                                print(result)
                            elif bill_type == 2:
                                amount = float(input("Enter the amount to pay for electricity bill: "))
                                result = bill_payment(user_id, 'electricity', amount)
                                print(result)
                            else:
                                print("Invalid choice")




elif option == 3:
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

                            chosen_time = input("Enter your desired appointment time: ")

                            if chosen_time in appointment_times and appointment_times[chosen_time] == 'yes':
                                print("Appointment scheduled!")
                                appointment_schedule[user_id] = chosen_time
                            else:
                                print("Sorry, appointment time is not available.")

                        elif option == 4:
                            username = input("Enter your username: ")
                            for user in data:
                                if user['username'] == username:
                                    if user['# of lines'] > 0:
                                        print(f"You have {user['# of lines']} notifications.")
                                    else:
                                        print("You don't have any notifications.")
                                    break


===========================================================================================================
##How to call the function
bill_payment(username)
if option == 3:
    bill_payment(username)


import pandas as pd

def bill_payment(username):
    data = pd.read_csv(r"C:\Users\ellac\OneDrive\Desktop\Python\Python_BankData.csv")

    user_data = data[data['username'] == username]

    if user_data.empty:
        print("User not found.")
        return

    print("Bill payment option selected.")
    print("Select an option:")
    print("1. Pay bill")
    print("2. View bill payment history")
    sub_option = input("Enter your choice (1 or 2): ")

    if sub_option == '1':
        print("Select a bill type:")
        print("1. Electricity")
        print("2. Water")
        print("3. Gas")
        bill_type_choice = input("Enter your choice (1 to 3): ")

        bill_types = ['electricity', 'water', 'gas']
        bill_type = bill_types[int(bill_type_choice) - 1]

        amount_to_pay = float(input(f"Enter the amount to pay for {bill_type}: "))

        initial_balance = user_data.loc[:, 'checking($)'].values[0]
        print(f"Initial balance in checking account: ${initial_balance}")

        confirmation = input(f"Confirm payment of ${amount_to_pay} for {bill_type}. Enter 'yes' to confirm: ")

        if confirmation.lower() == 'yes':
            
            data.loc[data['username'] == username, 'checking($)'] -= amount_to_pay
            updated_balance = data.loc[data['username'] == username, 'checking($)'].values[0]

            print(f"Payment of ${amount_to_pay} for {bill_type} successful.")
            print(f"Updated balance in checking account: ${updated_balance}")
            data[data['username'] == username] = user_data
            data.to_csv(r"C:\Users\ellac\OneDrive\Desktop\Python\Python_BankData.csv", index=False)
        else:
            print("Payment cancelled.")
        
    elif sub_option == '2':
        print(user_data.loc[:, 'bill history'].values[0])
    
    else:
        print("Invalid choice.")

