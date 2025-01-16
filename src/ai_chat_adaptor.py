import time
import re
import csv
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

def remove_invisible_chars(s: str) -> str:
    # Removes zero-width or invisible Unicode chars
    return re.sub(r'[\u200b-\u200d\uFEFF]', '', s).strip()

def main():
    # --- Set up the WebDriver ---
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')

    try:
        driver = uc.Chrome(options=options)
    except Exception as e:
        print(f"Error initialising the WebDriver: {e}")
        return

    driver.get("https://chat.openai.com/")
    print("Please log in, solve any CAPTCHA if needed, then press Enter to continue...")
    input("Press Enter after completing login...")

    input_csv = '../data/db/data_base_1001_to_5000.csv'
    output_csv = '../data/db/emails_1001_to_5000_part-1.csv'

    with open(input_csv, newline='', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(["Company Name", "Email Address"])
        next(reader, None)  # Skip the header row

        for row in reader:
            company_name = row[0].strip()
            prompt_text = (
                f"You are an advanced AI with the task of finding the **precise and exact contact email address** "
                f"for the company '{company_name}', located in Brisbane, Australia. "
                "1 - Your goal is to identify a **real, verified, and existing** email address directly associated "
                "with the company. 2 - You must **search exhaustively** (website, social media, press releases, etc.). "
                "3 - The email must be **valid** and not guessed. "
                "4 - Return exactly one result, as a plain email address. "
                "5 - If none exist, return **'email not found'** (no extra text). "
                "Your output must contain **only** that email or **'email not found'**."
            )

            # Send the prompt and capture its message ID
            old_ids = set(el.get_attribute("data-message-id") for el in driver.find_elements(By.XPATH, '//div[@data-message-author-role="assistant"]'))

            prompt_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@id="prompt-textarea" and @contenteditable="true"]'))
            )
            prompt_box.clear()
            prompt_box.send_keys(prompt_text)

            send_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Send prompt" and @data-testid="send-button"]'))
            )
            send_button.click()

            # Wait for the new assistant message with a unique ID and valid content
            retries = 3  # Number of retries for locating the element
            new_message = None

            for attempt in range(retries):
                try:
                    new_message = WebDriverWait(driver, 60).until(
                        lambda d: next(
                            (el for el in d.find_elements(By.XPATH, '//div[@data-message-author-role="assistant"]')
                             if el.get_attribute("data-message-id") not in old_ids and el.text.strip()),
                            None
                        )
                    )
                    if new_message:  # If successfully located, break out of the retry loop
                        break
                except StaleElementReferenceException:
                    print(f"StaleElementReferenceException encountered, retrying... (Attempt {attempt + 1}/{retries})")
                    time.sleep(1)  # Short delay before retrying

            if not new_message:
                print(f"Failed to locate the new message for {company_name} after {retries} attempts.")
                final_email = "email not found"
            else:
                # Extract the new message content
                html_content = new_message.get_attribute("innerHTML")
                soup = BeautifulSoup(html_content, "html.parser")

                # Extract email from the latest message
                markdown_div = soup.find("div", class_="markdown")
                if markdown_div:
                    p_tags = markdown_div.find_all("p")
                    if p_tags:
                        final_email = remove_invisible_chars(p_tags[0].get_text("", strip=True))
                    else:
                        final_email = "email not found"
                else:
                    final_email = "email not found"

            print(f"Processed: {company_name} => {final_email}")
            writer.writerow([company_name, final_email])
            time.sleep(2)

    driver.quit()

if __name__ == "__main__":
    main()
