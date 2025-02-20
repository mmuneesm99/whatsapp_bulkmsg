import os
import time
import pickle
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Load contacts from uploaded Excel file
def load_contacts(file_path):
    df = pd.read_excel(file_path)
    
    # Ensure correct column names
    if 'Number' not in df.columns or 'Message' not in df.columns:
        raise ValueError("Excel must have 'Number' and 'Message' columns.")

    return df['Number'].astype(str).tolist(), df['Message'].tolist()

# WhatsApp Automation
def send_whatsapp_messages(file_path):
    numbers, messages = load_contacts(file_path)

    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--user-data-dir=./chrome_data")  # Saves session

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://web.whatsapp.com/")

    session_file = "session.pkl"

    # Load session if available
    if os.path.exists(session_file):
        with open(session_file, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
    else:
        input("📷 Scan the QR Code and press ENTER to continue...")
        time.sleep(10)  # Wait for WhatsApp Web to load
        with open(session_file, "wb") as f:
            pickle.dump(driver.get_cookies(), f)

    # Send messages
    for number, message in zip(numbers, messages):
        print(f"Sending message to {number}...")

        driver.get(f"https://web.whatsapp.com/send?phone={number}&text={message}")
        time.sleep(5)  # Wait for WhatsApp to open chat

        send_button = driver.find_element("xpath", '//span[@data-icon="send"]')
        send_button.click()

        time.sleep(2)  # Wait before next message

    print("✅ All messages sent!")
    driver.quit()
