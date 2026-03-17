import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt

class AccountInfoWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Account Information")
        self.setGeometry(500, 250, 400, 420)
        layout = QVBoxLayout()
        title = QLabel("View Account Information")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)
        self.acc_input = QLineEdit()
        self.acc_input.setPlaceholderText("Enter Account Number")
        layout.addWidget(self.acc_input)
        view_button = QPushButton("View Account")
        view_button.clicked.connect(self.view_account)
        layout.addWidget(view_button)
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)
        self.setLayout(layout)

    def view_account(self):

        acc_no = self.acc_input.text().strip()
        if acc_no == "":
            QMessageBox.warning(self, "Error", "Please enter an account number.")
            return
        filename = f"{acc_no}.json"
        if not os.path.exists(filename):
            QMessageBox.warning(self, "Error", "Account does not exist.")
            return
        with open(filename, "r") as file:
            data = json.load(file)
        info = f"""
Full Name: {data['fname']} {data['mname']} {data['lname']}
Address: {data['address']}
Birthday: {data['birthday']}
Gender: {data['gender']}
Account Type: {data['type']}
Initial Deposit: {data['initial_deposit']}
Current Balance: {data['balance']}
"""
        self.result_box.setText(info)
