from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from db import getConnection  


class AccountInfoWindow(QWidget):
    goMenu = pyqtSignal() 

    def __init__(self, menu_window=None):  
        super().__init__()
        self.menu_window = menu_window
        self.setWindowTitle("View Account Information")
        self.setGeometry(500, 250, 400, 420)
        
        layout = QVBoxLayout()
        title = QLabel("Account Information")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.acc_input)
        
        view_btn = QPushButton("View Account")
        view_btn.clicked.connect(self.view_account)
        layout.addWidget(view_btn)
        
        self.result = QTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)
        
        back_btn = QPushButton("Go Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def view_account(self):
        acc_no = self.acc_input.text().strip()
        
        if not acc_no:
            QMessageBox.warning(self, "Input Error", "Please enter an account number")
            return

        conn = None
        cursor = None
        
        try:
            conn = getConnection()  
            if not conn:
                QMessageBox.critical(self, "Database Error", "Could not connect to database")
                return
                
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM accounts WHERE account_number=%s",
                (acc_no,)
            )

            account = cursor.fetchone()

            if not account:
                QMessageBox.warning(self, "Error", "Account not found")
                return

            info = f"""
Full Name: {account['first_name']} {account.get('middle_name', '')} {account['last_name']}
Address: {account['address']}
Birthday: {account['birthday']}
Gender: {account['gender']}
Account Type: {account['account_type']}
Current Balance: {account['balance']}
"""
            self.result.setText(info)

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def go_back(self):
        if self.menu_window:
            self.menu_window.show()
            self.close()
        else:
            self.goMenu.emit() 
