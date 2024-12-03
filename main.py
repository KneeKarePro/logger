import requests
import pandas as pd
import subprocess
import time
import numpy as np
from datetime import datetime

# ESP32 server details
ESP32_SSID = "KneeRehab"
ESP32_PASSWORD = "password"
ESP32_IP = "192.168.4.1"  # Replace with your ESP32 IP address
DNS_SERVER = "knee-rehab.local"  # Replace with your ESP32 hostname
DATA_ENDPOINT = f"http://{DNS_SERVER}/data"



class DataHandler:
    def __init__(self):
        self.ESP32_SSID = ESP32_SSID
        self.ESP32_PASSWORD = ESP32_PASSWORD
        
    def connect_to_wifi(self, ssid, password):
        return connect_to_wifi(ssid, password)
        
    def download(self):
        return download()
        
    def read_csv(self):
        return read_csv()
        
    def process_data(self, df):
        return process_data(df)
        
    def send_data_batched(self, df, user_id=1):
        return send_data_batched(df, user_id)
        
    def create_user(self, name, email, password):
        return create_user(name, password, email)

def main():
    from gui import KneeRehabGUI
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    data_handler = DataHandler()
    window = KneeRehabGUI(data_handler)
    window.resize(400, 500)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
