#TO BE BUILT SOON

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

class BalanceInquiryWindow(QWidget):pass
# balance_inquiry.py

# Sample database of accounts (you can expand this)
accounts = {
    "1001": 5000.00,
    "1002": 3200.50,
    "1003": 10000.00
}

def balance_inquiry():
    print("\n===== BALANCE INQUIRY =====")
    account_number = input("Enter your account number: ")

    # Check if account exists
    if account_number not in accounts:
        print("\nAccount does NOT exist. Returning to main menu...\n")
        return  # Goes back to caller (main menu)
    
    # If account exists, show balance
    balance = accounts[account_number]
    print(f"\nAccount Number: {account_number}")
    print(f"Current Balance: ₱{balance:.2f}\n")

def main():
    while True:
        print("===== MAIN MENU =====")
        print("[1] Balance Inquiry")
        print("[2] Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            balance_inquiry()
        elif choice == "2":
            print("\nExiting program... Goodbye!\n")
            break
        else:
            print("\nInvalid choice. Try again.\n")


if __name__ == "__main__":
    main()
