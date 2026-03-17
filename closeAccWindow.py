from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from db import getConnection  


class CloseAccWindow(QWidget):
    goMenu = pyqtSignal()  

    def __init__(self, menu_window=None):  
        super().__init__()
        self.menu_window = menu_window
        self.setWindowTitle("Close Account")
        self.setGeometry(500, 250, 350, 220)
        
        layout = QVBoxLayout()
        title = QLabel("Close Account")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.acc_input)
        
        close_btn = QPushButton("Close Account")
        close_btn.clicked.connect(self.close_account)
        layout.addWidget(close_btn)
        
        back_btn = QPushButton("Go Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
        
        self.setLayout(layout)

    def close_account(self):
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
            
            # Check if account exists and get balance
            cursor.execute(
                "SELECT balance FROM accounts WHERE account_number=%s",
                (acc_no,)
            )
            account = cursor.fetchone()

            if not account:
                QMessageBox.warning(self, "Error", "Account not found")
                return

            balance = account["balance"]

            confirm = QMessageBox.question(
                self,
                "Confirm Close Account",
                f"Remaining Balance: {balance}\n\nAre you sure you want to close this account?",
                QMessageBox.Yes | QMessageBox.No
            )

            if confirm == QMessageBox.Yes:
                
                cursor.execute(
                    "DELETE FROM transactions WHERE account_number=%s",
                    (acc_no,)
                )

                
                cursor.execute(
                    "DELETE FROM accounts WHERE account_number=%s",
                    (acc_no,)
                )
                
                conn.commit()
                
                QMessageBox.information(
                    self,
                    "Account Closed",
                    f"Account successfully closed.\nReturned Balance: {balance}"
                )
                
                self.go_back()  
                
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
            if conn:
                conn.rollback()
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
