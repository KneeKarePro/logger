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


def connect_to_wifi(ssid, password):
    try:
        # macOS command to connect to WiFi
        subprocess.run(
            ["networksetup", "-setairportnetwork", "en0", ssid, password], check=True
        )
        print(f"Connected to {ssid}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to {ssid}: {e}")
        return False
    return True


def download(url: str = DATA_ENDPOINT, filename: str = "knee_data.csv"):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Data saved to {filename}")
    return filename

def read_csv(filename: str = "knee_data.csv"):
    df = pd.read_csv(filename)
    # Turn unixtime to datatime
    df["Time"] = pd.to_datetime(df["Time"], unit="s") + pd.to_timedelta(
        df["Millis"], unit="ms"
    )
    return df

def process_data(df: pd.DataFrame):
    # Process data here
    # Rotation is the difference between the current angle and the previous angle over the time difference
    df["Rotation"] = df["Angle"].diff() / df["Time"].diff().dt.total_seconds()
    return df

def send_data(df: pd.DataFrame, user_id: int = 1):
    url = f"http://localhost:8000/users/{user_id}/knee-data"
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Rotation", "Angle", "Time"])
    df.dropna(subset=["Rotation", "Angle", "Time"], inplace=True)
    # NEED to send: user_id, timestamp, angle, rotation
    for i, row in df.iterrows():
        data = {
            "timestamp": row["Time"].timestamp(),
            "angle": row["Angle"],
            "rotation": row["Rotation"],
        }
        response = requests.post(url, json=data)
        print(response)

def send_data_batched(df: pd.DataFrame, user_id: int = 1):
    url = f"http://localhost:8000/users/{user_id}/knee-data/batch"
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Rotation", "Angle", "Time"])
    
    # Prepare batch data
    batch_data = [
        {
            "timestamp": row["Time"].timestamp(),
            "angle": row["Angle"],
            "rotation": row["Rotation"],
        }
        for _, row in df.iterrows()
    ]
    
    # Send in single request
    response = requests.post(url, json=batch_data)
    print(response.status_code) 


def main():
    # if connect_to_wifi(ESP32_SSID, ESP32_PASSWORD):
        # Wait for a few seconds to ensure connection is established
        # time.sleep(5)
        # filename = download()
    df = read_csv()
    df = process_data(df)
    send_data_batched(df)


if __name__ == "__main__":
    main()
