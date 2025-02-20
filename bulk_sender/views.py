from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import UploadedFile
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Load contacts from CSV
def load_contacts(file_path):
    df = pd.read_csv(file_path)
    return df['Number'].tolist(), df['Name'].tolist()

# Setup Selenium WebDriver with session persistence
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # Keeps browser open
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com")

    print("Waiting for WhatsApp Web login...")

    try:
        # Wait until the search bar is loaded (indicating successful login)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']"))
        )
        print("WhatsApp Web loaded successfully.")
    except Exception as e:
        print("Error: WhatsApp Web did not load. Exiting...")
        driver.quit()
        return None

    return driver

# Send messages
def send_message(driver, numbers, names, message):
    for number, name in zip(numbers, names):
        try:
            personalized_message = message.replace("{name}", name)
            url = f"https://web.whatsapp.com/send?phone={number}&text={personalized_message}"
            driver.get(url)

            # Wait for the send button to appear
            WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']"))
            ).click()

            print(f"Message sent to {name} ({number})")
            time.sleep(2)  # Prevents WhatsApp blocking

        except Exception as e:
            print(f"Failed to send message to {number}: {e}")

# Django view
def upload_file(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            file_path = uploaded_file.file.path
            custom_message = form.cleaned_data['message']  # Get user input message

            numbers, names = load_contacts(file_path)

            driver = setup_driver()
            if driver:
                send_message(driver, numbers, names, custom_message)
                driver.quit()

            os.remove(file_path)  # Clean up uploaded file after processing
            return redirect("success_page")

    else:
        form = FileUploadForm()

    return render(request, "upload.html", {"form": form})

def success_page(request):
    return render(request, "success.html")
