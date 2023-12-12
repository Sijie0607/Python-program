import csv

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




import csv
import sys

# Function to verify user credentials
def verify_credentials(username, password, user_data):
    return user_data.get(username) == password ##

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
