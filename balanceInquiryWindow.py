#TO BE BUILT SOON

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout,
QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
import mysql.connector
from mysql.connector import Error
from config import dbconfig
class BalanceInquiryWindow(QWidget):pass

 
class balanceInquiryWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Balance Inquiry - IT001_Carabao Bank")
        self.setFixedSize(350, 200)

        # UI Elements
        self.label = QLabel("Enter Account Number:")
        self.label.setAlignment(Qt.AlignCenter)

        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("Account Number")

        self.check_button = QPushButton("Check Balance")
        self.check_button.clicked.connect(self.check_balance)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.account_input)
        layout.addWidget(self.check_button)

        self.setLayout(layout)


    # ------------------------------------------
    # MYSQL CONNECTION (uses your config.py)
    # ------------------------------------------
    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host=dbconfig["host"],
                user=dbconfig["user"],
                password=dbconfig["password"],
                database=dbconfig["database"]
            )
            return conn
        except Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
            return None


    # ------------------------------------------
    # BALANCE INQUIRY LOGIC
    # ------------------------------------------
    def check_balance(self):
        account_number = self.account_input.text().strip()

        if account_number == "":
            QMessageBox.warning(self, "Missing Input", "Please enter an account number.")
            return

        conn = self.connect_db()
        if conn is None:
            return

        try:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT current_balance 
                FROM accounts 
                WHERE account_number = %s
            """

            cursor.execute(query, (account_number,))
            result = cursor.fetchone()

            if result is None:
                QMessageBox.critical(self, "Not Found", "Account does not exist.")
                return

            balance = float(result["current_balance"])

            QMessageBox.information(
                self,
                "Balance Inquiry",
                f"Account Number: {account_number}\nCurrent Balance: ₱{balance:,.2f}"
            )

        except Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            conn.close()
