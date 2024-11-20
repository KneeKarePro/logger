import requests
import pandas as pd
import subprocess
import time

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


def main():
    if connect_to_wifi(ESP32_SSID, ESP32_PASSWORD):
        # Wait for a few seconds to ensure connection is established
        time.sleep(5)
        response = requests.get(DATA_ENDPOINT)
        filename = "knee_data.csv"
        print(response)
        # response.content looks like bytes = b'Time,Angle\r\n<unixtime int>,<angle int>\n,...
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Data saved to {filename}")
        df = pd.read_csv(filename)
        # Turn unixtime to datatime
        df["Time"] = pd.to_datetime(df["Time"], unit="s")
        print(df)


if __name__ == "__main__":
    main()
