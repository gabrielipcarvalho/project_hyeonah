import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# Set up undetected Chrome WebDriver
options = uc.ChromeOptions()
options.headless = False  # Set to True if headless mode is desired
options.add_argument('--no-sandbox')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--start-maximized')

# Initialize the WebDriver
try:
    driver = uc.Chrome(options=options)
except Exception as e:
    print(f"Error initializing the WebDriver: {e}")
    exit()

# Open ChatGPT login page
driver.get('https://chat.openai.com/')
print("Please log in and complete any CAPTCHA, then press Enter to continue...")
input("Press Enter after completing login...")  # Pauses the script until login is complete

# Load company names from CSV
input_csv = '../data/db/complete_data_base.csv'
output_csv = '../data/db/testing.csv'

with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["Company Name", "Email Address"])

    next(reader, None)  # Skip header row if present

    for row in reader:
        company_name = row[0]
        prompt = (
            f"You are tasked with finding the precise and exact contact email for the company '{company_name}' located in Brisbane, Australia. "
            "Use all resources available to you and try as hard as possible to find a real, existing email. "
            "The email must be accurate and real, not made up or fabricated. "
            "If you cannot find a precise email, return exactly the phrase 'email not found'. "
            "Your response must only contain either the email address or 'email not found' without any other strings, explanations, or details."
        )

        for attempt in range(3):  # Retry logic, up to 3 attempts
            try:
                # Locate the input field and send the prompt
                input_field = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@id="prompt-textarea" and @contenteditable="true"]'))
                )
                input_field.send_keys(prompt)

                # Locate and click the send button
                send_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send prompt" and @data-testid="send-button"]'))
                )
                send_button.click()

                # Wait for the response to load using explicit wait
                response_element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message")]'))
                )

                # Retrieve the last response
                response = driver.find_elements(By.XPATH, '//div[contains(@class, "message")]')[-1]
                email = response.text.strip()
                writer.writerow([company_name, email])
                print(f"Processed: {company_name} -> {email}")
                break  # Exit retry loop on success

            except Exception as e:
                print(f"Retry {attempt + 1} failed for {company_name}: {e}")
                time.sleep(5)  # Wait before retrying
                if attempt == 2:
                    writer.writerow([company_name, "Error"])

        time.sleep(10)  # Increased rate limiting to avoid being flagged
