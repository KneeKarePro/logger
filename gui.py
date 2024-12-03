from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PySide6.QtCore import Qt
import sys

class KneeRehabGUI(QMainWindow):
    def __init__(self, data_handler):
        super().__init__()
        self.data_handler = data_handler
        self.setWindowTitle("Knee Rehabilitation Data Manager")
        self.setup_ui()

    def setup_ui(self):
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add title label
        title_label = QLabel("Knee Rehabilitation Data Manager")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Add user creation section
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter username")
        layout.addWidget(self.name_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email")
        layout.addWidget(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        create_user_btn = QPushButton("Create User")
        create_user_btn.clicked.connect(self.create_user)
        layout.addWidget(create_user_btn)

        # Add data collection buttons
        collect_btn = QPushButton("Collect Data")
        collect_btn.clicked.connect(self.collect_data)
        layout.addWidget(collect_btn)

        process_btn = QPushButton("Process and Send Data")
        process_btn.clicked.connect(self.process_and_send)
        layout.addWidget(process_btn)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

    def create_user(self):
        try:
            user_id = self.data_handler.create_user(
                name=self.name_input.text(),
                email=self.email_input.text(),
                password=self.password_input.text()
            )
            self.status_label.setText(f"User created successfully! ID: {user_id}")
        except Exception as e:
            self.status_label.setText(f"Error creating user: {str(e)}")

    def collect_data(self):
        try:
            if self.data_handler.connect_to_wifi(self.data_handler.ESP32_SSID, self.data_handler.ESP32_PASSWORD):
                filename = self.data_handler.download()
                self.status_label.setText(f"Data collected and saved to {filename}")
            else:
                self.status_label.setText("Failed to connect to ESP32")
        except Exception as e:
            self.status_label.setText(f"Error collecting data: {str(e)}")

    def process_and_send(self):
        try:
            df = self.data_handler.read_csv()
            df = self.data_handler.process_data(df)
            self.data_handler.send_data_batched(df)
            self.status_label.setText("Data processed and sent successfully!")
        except Exception as e:
            self.status_label.setText(f"Error processing data: {str(e)}")

