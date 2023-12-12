import csv
import sys

# Function to verify user credentials
def verify_credentials(username, password, user_data):
    return user_data.get(username) == password

# Load user data from CSV 
def load_user_data(csv_file_path):
    user_data = {}

    # Read CSV and process data
    with open(csv_file_path, mode = 'r') as file:     
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            username = row["username"]
            password = row["password"]
            # Store the username as key and password as value in the dictionary
            user_data[username] = password
    return user_data
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
