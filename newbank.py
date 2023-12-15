import pandas as pd
import sys
from datetime import datetime
file_path = r"C:\Users\ellac\OneDrive\Desktop\Python_BankData.csv"
bankfile = pd.read_csv(file_path)

# Function for handling Bill Payment (It takes username as input)
def bill_payment(username):
    print("Please select an option from below:")  #Displays bill options and prompts the user for an input
    print("1. Pay bill")
    print("2. View bill payment history")
    sub_option = input("Please enter your choice (1 or 2): ")

    if sub_option == '1':
        print("Select a bill type:")    #Displays bill options and prompts user for an input
        print("1. Electricity")
        print("2. Water")
        bill_type_choice = input("Please enter your choice (1 or 2): ")

        bill_types = ['electricity', 'water']
        bill_type = bill_types[int(bill_type_choice) - 1]        # change the string number into int number, and match electricity with 1-1 and water with 2-1

        amount_to_pay = float(input(f"Please enter the amount to pay for {bill_type}: $")) 

        initial_balance = bankfile.loc[:, 'checking($)'].values[0]        # locate checking balance in csv
        print(f"Available balance in checking account: ${initial_balance}")

        confirmation = input(f"Please enter 'yes' to confirm payment of ${amount_to_pay} for {bill_type}: ")

        if confirmation.lower() == 'yes':        # make sure user input is either case of yes
            if initial_balance > amount_to_pay:        # if balance > amount needs to be paid, subtract the amount from balance and update
                bankfile.loc[bankfile['username'] == username, 'checking($)'] -= amount_to_pay
                updated_balance = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
                print(f"Payment of ${amount_to_pay} for {bill_type} successful.")
                print(f"Updated balance in checking account: ${updated_balance}")
                bankfile[bankfile['username'] == username] = bankfile
                bankfile.to_csv(r"C:\Users\ellac\OneDrive\Desktop\Python_BankData.csv", index=False)
            else:
                print('Insufficient Balance')        # if balance < amount needs to be paid
        else:
            print("Payment cancelled.")        # if confirmation is not yes, cancel payment

    elif sub_option == '2':
        print(bankfile.loc[:, 'bill history'].values[0])        # locate bill history in csv

    else:
        print("Invalid choice.")


#========================================================================================================
# Function to check credit payment due date for a user (Takes username as input)
def check_credit_payment(username):
    credit_amount = bankfile.loc[bankfile['username'] == username, 'Credit Amount'].values[0]  # Fetch credit amount for the given username from the bankfile
    
    # Determine the due date for credit payment (always due on the 25th of each month)
    today = datetime.now()
    if today.day >= 25:    # If current day is 25th or later in the month
        next_payment_date = datetime(today.year, today.month + 1, 25)  # Next payment is in the following month on the 25th
    else:
        next_payment_date = datetime(today.year, today.month, 25)  # Next payment is in the current month on the 25th 

    days_until_payment = (next_payment_date - today).days  # Calculate the number of days until the next credit payment is due
    
    if days_until_payment == 0:    # Display the information regarding the due date of the credit payment
        print(f"Payment for credit amount ${credit_amount} is due today!")
    else:
        print(f"Your next credit payment of ${credit_amount} is due in {days_until_payment} days.")


#========================================================================================================
#Function to handle funds transfer
def moneytransfer(username):
    user_choice = int(input('Please enter 1 for Internal Transfer or 2 for External Transfer:'))

    if user_choice == 1:
        saving = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0]
        checking = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
        print(f'Savings balance: ${saving:.2f}')
        print(f'Checking balance: ${checking:.2f}')

        print('1. Checking to Savings.')
        print('2. Savings to Checking.')
        s_or_ch = input('Please input your choice: ')

        if s_or_ch == "1":
            amount1 = float(input('How much money would you like to transfer:'))
            
            if amount1 <= checking:
                new_checking = checking - amount1
                new_saving = saving + amount1

                print('Transfer successful')
                print(f'Your new savings account balance is ${new_saving:.2f}')
                print(f'Your new current account balance is ${new_checking:.2f}')
                bankfile.loc[bankfile['username'] == username, 'saving($)'] = new_saving
                bankfile.loc[bankfile['username'] == username, 'checking($)'] = new_checking
                bankfile.to_csv("C:\\Users\\hw\\Desktop\\python\\Python_BankDatafinal.csv", index=False)

            else:
                print("Insufficient Funds!")

        elif s_or_ch == "2":
            amount1 = float(input('How much money would you like to transfer:'))
            
            if amount1 <= saving:
                new_saving = saving - amount1
                new_checking = checking + amount1
                print('Transfer successful')
                print(f'Your new savings account balance is ${new_saving:.2f}')
                print(f'Your new current account balance is ${new_checking:.2f}')
                bankfile.loc[bankfile['username'] == username, 'saving($)'] = new_saving
                bankfile.loc[bankfile['username'] == username, 'checking($)'] = new_checking
                bankfile.to_csv("C:\\Users\\hw\\Desktop\\python\\Python_BankDatafinal.csv", index=False)
            else:
                print("Insufficient Funds!")
        else:
            print("Invalid Input!")

    elif user_choice == 2:
        checking = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
        print(f'Checking balance: ${checking:.2f}')
        external_account = input('Please input the account number you want to transfer to:')
        
        if len(external_account) == 10:
            amount2 = float(input('Please input the amount you want to transfer:'))
            
            if amount2 > checking:
                print("Insufficient Funds!")
                
            elif amount2 <= checking and amount2 <= 2000:
                new_checking = checking - amount2
                print('Transfer successful')
                print(f'Your new current account balance is ${new_checking:.2f}')
                bankfile.loc[bankfile['username'] == username, 'checking($)'] = new_checking
                bankfile.to_csv("C:\\Users\\hw\\Desktop\\python\\Python_BankDatafinal.csv", index=False)

            elif amount2 > 2000:
                print('A PIN has been sent to your phone number')
                pin = int(input('Please input the PIN:'))

                if pin == 0:
                    new_checking = checking - amount2
                    print('Transfer successful')
                    print(f'Your new current account balance is ${new_checking:.2f}')
                    bankfile.loc[bankfile['username'] == username, 'checking($)'] = new_checking
                    bankfile.to_csv("C:\\Users\\hw\\Desktop\\python\\Python_BankDatafinal.csv", index=False)

                else:
                    print('Invalid Pin')
        else:
            print('Invalid account number. Please enter a 10-digit account number.')

#==============================================================================================================================
# Function to handle loan application
def loanapply(username):
    account_number = bankfile.loc[bankfile['username'] == username, 'account number'].values[0]
    credit_score = bankfile.loc[bankfile['account number'] == account_number, 'credit score'].values[0]
    print(f'Your credit score is: {credit_score}')
    if credit_score <= 600:
        print('Not enough credit score')
    else:
        loan_amount = float(input('Please enter the loan amount you need:'))
        saving_amount = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0]
        loan_to_saving_ratio = loan_amount / saving_amount
        if loan_to_saving_ratio >= 2:
            print('Sorry. You cannot apply for a loan now.')
        else:
            print('Please submit your documents to the bank.')

#==============================================================================================================================
Function for handling appointments
# Initialize a dictionary to store appointments
appointment_schedule = {}
def schedule_appointment(username):
    if username in appointment_schedule:
        print(f"Your scheduled appointment: {appointment_schedule[username]}")

        change_appointment = input("Do you want to change your appointment time? (yes/no): ").lower()
        if change_appointment == 'yes':
            appointment_times = {
                '9AM': 'yes',
                '11AM': 'yes',
                '1PM': 'yes',
                '3PM': 'yes'
            }

            previous_time = appointment_schedule[username]
            appointment_times[previous_time.upper()] = 'yes'  # Make the previous appointment time available again

            print("Available appointment times:")
            available_times = [time for time, status in appointment_times.items() if status == 'yes']
            for time in available_times:
                print(time)

            chosen_time = input("Please enter your desired appointment time: ").upper()

            while chosen_time.upper() not in [time.upper() for time in appointment_times] or appointment_times[chosen_time.upper()] != 'yes':
                print("Invalid choice or appointment time not available.")
                chosen_time = input("Please select another appointment time: ").upper()

            print("Appointment changed!")
            appointment_schedule[username] = chosen_time.upper()  # Store the new appointment time in the dictionary
            appointment_times[chosen_time.upper()] = 'no'  # Mark the chosen time as unavailable

        return

    else:
        appointment_times = {
            '9AM': 'yes',
            '11AM': 'yes',
            '1PM': 'yes',
            '3PM': 'yes'
        }

        print("Available appointment times:")
        available_times = [time for time, status in appointment_times.items() if status == 'yes']
        if not available_times:
            print("No available appointment times.")
            return

        for time in available_times:
            print(time)

        chosen_time = input("Please enter your desired appointment time (or 'cancel' to cancel appointment): ").upper()

        if chosen_time.lower() == 'cancel':
            print("Appointment canceled.")
            return

        while chosen_time.upper() not in [time.upper() for time in appointment_times] or appointment_times[chosen_time.upper()] != 'yes':
            print("Invalid choice or appointment time not available.")
            chosen_time = input("Please select another appointment time (or 'cancel' to cancel appointment): ").upper()

        print("Appointment scheduled!")
        appointment_schedule[username] = chosen_time.upper()  # Store the appointment in the dictionary
        appointment_times[chosen_time.upper()] = 'no'  # Mark the chosen time as unavailable for other users
#==============================================================================================================================
# Function for balance enquiry (Takes username as input)
def balance_enquiry(username):
    user_data = bankfile[bankfile['username'] == username]    # Fetch user data based on the provided username from bankfile
    print("Select an account type:")   # Display options for the user to select the account type
    print("1. Checking")
    print("2. Savings")
    account_choice = input("Please enter your choice (1 or 2): ")
    
    if account_choice == '1':   # Retrieve and display the checking account balance for the user
        checking_balance = user_data['checking($)'].values[0]
        print(f"Checking account balance for {username}: ${checking_balance}")
    elif account_choice == '2':    # Retrieve and display the savings account balance for the user
        savings_balance = user_data['saving($)'].values[0]
        print(f"Savings account balance for {username}: ${savings_balance:.2f}")
    else:
        print("Invalid choice.")


# ======================================================================================================================
# Function for handling login credentials
def verify_credentials(username, password, bankfile):        
    return str(bankfile.loc[bankfile['username'] == username, 'password'].values[0]) == password        # locate username in the csv and match the password
                                                                                                        
def verify_credentials_code(username, third_platform_code, bankfile):
    return str(bankfile.loc[bankfile['username'] == username, 'third_platform_code'].values[0]) == third_platform_code        # match third platform code



#Main Menu function
def displayMenu():
    print("1. Money Transfer")
    print("2. Bill Payment")
    print("3. Appointment")
    print("4. Notification")
    print("5. Loans")
    print("6. Balance Enquiry")
    print("7. Exit")
    choice = input("Please enter your choice: ")
    return choice
#===============================================================================================================
#Account Access function
def Accountaccess():
    username_attempts = 0
    password_attempts = 0
    tp_code_attempts = 0
    
    while username_attempts < 3:        # username can be input three times
        username = input("Please enter your username: ")
        
        if username in bankfile['username'].values:       
            while password_attempts < 3:        # password can be input three times
                password = input("Please enter your password: ")
                
                if verify_credentials(username, password, bankfile):
                    while tp_code_attempts < 3:        # tp code can be input three times
                        third_platform_code = input("Please enter the third-platform code: ")
                        
                        if verify_credentials_code(username, third_platform_code, bankfile):        # if username, password, tp code are all correct
                            print(f"Hi {username}, Welcome!")
                            # Displaying the menu options after successful login
                            while True:
                                choice = displayMenu()
                                
                                if choice == '1':
                                    moneytransfer(username)
                                elif choice == '2':
                                    bill_payment(username)
                                elif choice == '3':
                                    schedule_appointment(username)
                                elif choice == '4':
                                    check_credit_payment(username)
                                elif choice == '5':
                                    accountnumber = int(input('Please enter your account number: '))
                                    loanapply(accountnumber)
                                elif choice == '6':
                                    balance_enquiry(username)
                                elif choice == '7':
                                    sys.exit('Thank you for banking with us!')
                                else:
                                    print("Invalid choice.")
                            return  
                        else:
                            tp_code_attempts += 1
                            print("Third-platform code incorrect.")
                            
                    print("Maximum third-platform code attempts reached.")
                    return  # Exit if max third-platform code attempts are reached
                
                else:
                    password_attempts += 1
                    print("Incorrect password.")
                    
            print("Maximum password attempts reached.")
            return  # Exit if max password attempts are reached
            
        else:
            username_attempts += 1
            print("Incorrect username.")
            
    print("Maximum username attempts reached. Your account is blocked. Please visit our nearest branch for assistance")


def main():
    Accountaccess()
    

if __name__ == "__main__":
    main()
