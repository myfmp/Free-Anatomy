# Import the required modules
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
import os
import whisper
import warnings
from tempmail import EMail
from bs4 import BeautifulSoup
import re
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


warnings.filterwarnings("ignore")

def transcribe(url):
    with open('.temp', 'wb') as f:
        f.write(requests.get(url).content)
    result = model.transcribe('.temp')
    return result["text"].strip()

def request_audio_version(driver):
    driver.switch_to.default_content()
    driver.switch_to.frame(driver.find_element(By.XPATH, ".//iframe[@title='recaptcha challenge expires in two minutes']"))
    driver.find_element(By.ID, "recaptcha-audio-button").click()

def solve_audio_captcha(driver):
    try:
        # Wait for the audio element with ID "audio-source" to be present
        audio_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "audio-source"))
        )
        # Transcribe the audio source
        text = transcribe(audio_element.get_attribute('src'))

        # Wait for the input field with ID "audio-response" to be clickable
        response_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "audio-response"))
        )
        # Enter the transcribed text into the input field
        response_input.send_keys(text)

        # Wait for the button with ID "recaptcha-verify-button" to be clickable
        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "recaptcha-verify-button"))
        )
        # Click the verify button
        verify_button.click()
    except Exception as e:
        print(f"Error: {e}")
        # Handle the error as needed, such as logging or raising an exception

def RunBot():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Run in headless mode
    # Initialize the WebDriver with Chrome options
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    driver.get("https://store.3d4medical.com/account")
    # Click the specified element
    driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div[2]/div/div[3]/button").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div/div[2]/div/button").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[3]/button/span").click()
    time.sleep(1)
    email = EMail()
    tabs = driver.window_handles
    driver.switch_to.window(tabs[1])
    time.sleep(3)
    input_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[2]/input")))
    input_field = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[2]/input")
    input_field.send_keys(str(email))
    input_field.submit()
    time.sleep(1)
    input_field_2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[2]/input")))
    input_field_2 = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/form/div[1]/div/div/div/div/div[2]/input")
    input_field_2.send_keys("BOB")
    random_number = random.randint(1, 10000)
    password = f"Malibou{random_number}"
    input_field_3 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/form/div[3]/div/div/div/div/div/div[1]/div/div/div[2]/input")))
    input_field_3 = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/form/div[3]/div/div/div/div/div/div[1]/div/div/div[2]/input")
    input_field_3.send_keys(password)
    input_field_3.submit()
    time.sleep(5)
    request_audio_version(driver)
    time.sleep(5)
    solve_audio_captcha(driver)
    msg = email.wait_for_message()
    # Parse the email body with BeautifulSoup
    soup = BeautifulSoup(msg.body, 'html.parser')
    # Define a regex pattern to find the URL
    pattern = re.compile(r'https://accounts\.3d4medical\.com/verify/\w+/')
    # Search for the pattern in the HTML content
    match = pattern.search(msg.body)
    # Extract the URL if found
    verification_url = match.group(0) if match else None
    account = [str(email),password,verification_url]
    time.sleep(5)
    driver.quit()
    return account

