import pandas as pd
import sys
from datetime import datetime
file_path = r"C:\Users\ellac\OneDrive\Desktop\Python_BankData.csv"
bankfile = pd.read_csv(file_path)


def bill_payment(username):
    print("Please select an option from below:")
    print("1. Pay bill")
    print("2. View bill payment history")
    sub_option = input("Please enter your choice (1 or 2): ")

    if sub_option == '1':
        print("Select a bill type:")
        print("1. Electricity")
        print("2. Water")
        bill_type_choice = input("Please enter your choice (1 or 2): ")

        bill_types = ['electricity', 'water']
        bill_type = bill_types[int(bill_type_choice) - 1]

        amount_to_pay = float(input(f"Please enter the amount to pay for {bill_type}: $"))

        initial_balance = bankfile.loc[:, 'checking($)'].values[0]
        print(f"Available balance in checking account: ${initial_balance}")

        confirmation = input(f"Please enter 'yes' to confirm payment of ${amount_to_pay} for {bill_type}: ")

        if confirmation.lower() == 'yes':
            if initial_balance > amount_to_pay:
                bankfile.loc[bankfile['username'] == username, 'checking($)'] -= amount_to_pay
                updated_balance = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
                print(f"Payment of ${amount_to_pay} for {bill_type} successful.")
                print(f"Updated balance in checking account: ${updated_balance}")
                bankfile[bankfile['username'] == username] = bankfile
                bankfile.to_csv(r"C:\Users\ellac\OneDrive\Desktop\Python_BankData.csv", index=False)
            else:
                print('Insufficient Balance')
        else:
            print("Payment cancelled.")

    elif sub_option == '2':
        print(bankfile.loc[:, 'bill history'].values[0])

    else:
        print("Invalid choice.")



def check_credit_payment(username):
    credit_amount = bankfile.loc[bankfile['username'] == username, 'Credit Amount'].values[0]
    
    # Credit payment is due on the 25th day of every month
    today = datetime.now()
    if today.day >= 25:
        next_payment_date = datetime(today.year, today.month + 1, 25)
    else:
        next_payment_date = datetime(today.year, today.month, 25)

    days_until_payment = (next_payment_date - today).days
    
    if days_until_payment == 0:
        print(f"Payment for credit amount ${credit_amount} is due today!")
    else:
        print(f"Your next credit payment of ${credit_amount} is due in {days_until_payment} days.")


========================================================================================================
def moneytransfer(username):
    user_choice = int(input('Please enter 1 for Internal Transfer or 2 for External Transfer:'))  #let user know there are two choices to transfer money

    if user_choice == 1:
        saving = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0]  #Select the column"saving" where your row in dataframe(bankfile) meet the condition 'username'= the user input  
        checking = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]  #value[0] means select unique values after row and column filtering
        print(f'Savings balance: ${saving:.2f}') 
        print(f'Checking balance: ${checking:.2f}')

        print('1. Checking to Savings.') 
        print('2. Savings to Checking.')  # Can choose to withdrawals from both savings and checking accounts, resulting in changes in the respective columns' values in the CSV file.
        s_or_ch = input('Please input your choice: ')

        if s_or_ch == "1":
            amount1 = float(input('How much money would you like to transfer:'))  
            
            if amount1 <= checking:        #  If condition will make sure the user's input amount need to less than the balance in their account eotherwise it will show the hit to notify the insufficient money
                new_checking = checking - amount1  
                new_saving = saving + amount1      #Assigning values to the new account balances
                print('Transfer successful')
                print(f'Your new savings account balance is ${new_saving:.2f}')
                print(f'Your new current account balance is ${new_checking:.2f}')
                bankfile.loc[bankfile['username'] == username, 'saving($)'] = new_saving
                bankfile.loc[bankfile['username'] == username, 'checking($)'] = new_checking   #Both account balances will change simultaneously，Assign new values back to the dataframe in the original position
                bankfile.to_csv("C:\\Users\\hw\\Desktop\\python\\Python_BankDatafinal.csv", index=False) #Update the new value to CSV file and the file while remain these new value which will be used next time as the minuend..

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
                print("Insufficient Funds!") # when user choose 2 under the outer if loop，just change direction of transfer and the other part remain same.
                
        else:
            print("Invalid Input!")  # under this outer if loop, if user input other number, it will prompt the user with an invalid option.

    elif user_choice == 2: # the elif is parallel to the outer if loop，user choose to do a external transfer, our default set for the external transfer is from checking account.
        checking = bankfile.loc[bankfile['username'] == username, 'checking($)'].values[0]
        print(f'Checking balance: ${checking:.2f}')
        external_account = input('Please input the account number you want to transfer to:') 
        
        if len(external_account) == 10: # Nesting a if condition to constraint the account number's format
            amount2 = float(input('Please input the amount you want to transfer:'))
            if amount2 > checking:
                print("Insufficient Funds!")   
            elif amount2 <= checking and amount2 <= 2000: # When the user's input amount is lower than the account balance and it is less than 2000(default benchmark),processing following code 
                new_checking = checking - amount2  # renewing the checking balance 
                print('Transfer successful')
                print(f'Your new current account balance is ${new_checking:.2f}')
                bankfile.loc[bankfile['username'] == username, 'checking($)'] = new_checking
                bankfile.to_csv("C:\\Users\\hw\\Desktop\\python\\Python_BankDatafinal.csv", index=False) # Assign new value to the CSv File and deposit the new value in certain position.
            elif amount2 > 2000:                          # if the user's input ammount to do a external transfer is larger than 2000, the Pin code will be send to the user's phone
                print('A PIN has been sent to your phone number')
                pin = int(input('Please input the PIN:')) 
                if pin == 0:                               # Here we just assume the pin is 0 which been sent to the user.
                    new_checking = checking - amount2
                    print('Transfer successful')
                    print(f'Your new current account balance is ${new_checking:.2f}')
                    bankfile.loc[bankfile['username'] == username, 'checking($)'] = new_checking
                    bankfile.to_csv("C:\\Users\\hw\\Desktop\\python\\Python_BankDatafinal.csv", index=False)

                else:
                    print('Invalid Pin')
        else:
            print('Invalid account number. Please enter a 10-digit account number.')

==============================================================================================================================
def loanapply(username):                                                                         # In logic, the credit score is associate with their account number
    account_number = bankfile.loc[bankfile['username'] == username, 'account number'].values[0]  # choose the 'account number'column and the row  where 'username' = user's username input in the dataframe
    credit_score = bankfile.loc[bankfile['account number'] == account_number, 'credit score'].values[0]  # choose the 'credit scores 'column and the row  where 'account number' =  account_number in the dataframe
    print(f'Your credit score is: {credit_score}')
    if credit_score <= 600:
        print('Not enough credit score')
    else:
        loan_amount = float(input('Please enter the loan amount you need:'))
        saving_amount = bankfile.loc[bankfile['username'] == username, 'saving($)'].values[0] 
        loan_to_saving_ratio = loan_amount / saving_amount            # Calculating the ratio of loan amount over saving amount to do an initial filtering 
        if loan_to_saving_ratio >= 2:                                  # 2 is the benchmark that bank set as an index 
            print('Sorry. You cannot apply for a loan now.')
        else:
            print('Please submit your documents to the bank.')


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
    print("6. Balance Enquiry")
    print("7. Exit")
    choice = input("Please enter your choice: ")
    return choice

def Accountaccess():
    username_attempts = 0
    password_attempts = 0
    tp_code_attempts = 0
    
    while username_attempts < 3:
        username = input("Please enter your username: ")
        
        if username in bankfile['username'].values:
            while password_attempts < 3:
                password = input("Please enter your password: ")
                
                if verify_credentials(username, password, bankfile):
                    while tp_code_attempts < 3:
                        third_platform_code = input("Please enter the third-platform code: ")
                        
                        if verify_credentials_code(username, third_platform_code, bankfile):
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
            
    print("Maximum username attempts reached. Your account is blocked.")


def main():
    Accountaccess()
    

if __name__ == "__main__":
    main()
