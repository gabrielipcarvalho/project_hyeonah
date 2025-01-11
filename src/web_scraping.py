"""
Author: Gabriel Isaiah Padus-Carvallion
Date: 03-01-2025

Description:
This script automates the process of logging into LinkedIn, navigating through the pages of company search results,
and scraping the company names into a CSV file. The script performs the following tasks:

1. Loads LinkedIn credentials from environment variables stored in a `.env` file.
2. Sets up a Selenium WebDriver with Chrome in headless mode for browsing.
3. Logs into LinkedIn using provided credentials.
4. Scrapes company names from multiple LinkedIn search result pages (pages 1 to 82) based on a set of predefined search parameters.
5. Appends the scraped company names to a CSV file (`data_base_11_to_500.csv`) under the "Name" column, with the "Email" column left empty.
6. Implements basic error handling, logging, and rate-limiting to avoid detection.
7. Closes the browser session after the scraping process is completed.

Notes:
- The CSV file is assumed to already exist and contains a header row ["Name", "Email"].
- The file paths are previously defined; if you ever change the file paths, remember to change them here too.

Dependencies:
- selenium
- webdriver_manager
- dotenv
"""

####################################################
# LET'S PLAY WITH MAGIC
####################################################
import time
import csv
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ------------------------------------------------------------------
# 1) Load environment variables from .env file
# ------------------------------------------------------------------
load_dotenv()  # This will read the .env file and load the variables into the environment

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")  # Get the email from environment
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")  # Get the password from environment

if not LINKEDIN_EMAIL or not LINKEDIN_PASSWORD:
    raise ValueError("Missing LinkedIn credentials. Please check your .env file.")

# ------------------------------------------------------------------
# 2) BASE URLS & HEADERS
# ------------------------------------------------------------------
SEARCH_BASE_URL = (
    "https://www.linkedin.com/search/results/companies/"
    "?companyHqGeo=%5B%22104468365%22%5D"
    "&companySize=%5B%22H%22%2C%22I%22%5D"
    "&origin=FACETED_SEARCH"
    "&page={page_num}"
)

# ------------------------------------------------------------------
# 3) SETUP A SELENIUM DRIVER
# ------------------------------------------------------------------
def setup_driver():
    """Setup Chrome WebDriver with Selenium."""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (without opening browser window)
    options.add_argument("--disable-gpu")  # Disable GPU (helps in headless mode)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# ------------------------------------------------------------------
# 4) LOGIN TO LINKEDIN USING SELENIUM
# ------------------------------------------------------------------
def linkedin_login(driver, email, password):
    """Logs into LinkedIn using Selenium."""
    driver.get("https://www.linkedin.com/login")

    # Wait for the email field to be available and enter the email
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username"))).send_keys(email)

    # Wait for the password field to be available and enter the password
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password"))).send_keys(password)

    # Click the login button
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for login to complete (check if the homepage is loaded)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "global-nav-search")))

    print("Successfully logged into LinkedIn!")
    
# ------------------------------------------------------------------
# 5) SCRAPE COMPANIES FROM A SINGLE PAGE
# ------------------------------------------------------------------
def scrape_companies_from_page(driver):
    """Scrapes company names from the current page."""
    company_names = []
    
    # Target <a> tags in the textual block that contains the company name:
    # //div[contains(@class,'t-roman t-sans')]
    #    //a[@data-test-app-aware-link and contains(@href,'/company/')]
    anchor_tags = driver.find_elements(
        By.XPATH,
        "//div[contains(@class,'t-roman t-sans')]"
        "//a[@data-test-app-aware-link and contains(@href,'/company/')]"
    )

    for tag in anchor_tags:
        name = tag.text.strip()
        if name:
            company_names.append(name)

    return company_names

# ------------------------------------------------------------------
# 6) MAIN SCRAPING LOGIC
# ------------------------------------------------------------------
def main():
    # 6a. Set up the Selenium WebDriver
    driver = setup_driver()

    try:
        # 6b. Login to LinkedIn
        linkedin_login(driver, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)

        # 6c. Open the CSV in append mode
        csv_path = "../data/db/data_base_5001_to_infinity.csv"  # Adjust if your relative path is different
        with open(csv_path, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Assumes the header row ["Name", "Email"] is already in place.

            # 6d. Scrape the pages
            for page_num in range(1, 38):  # Pages 1 through 37
                url = SEARCH_BASE_URL.format(page_num=page_num)
                print(f"Scraping page {page_num} -> {url}")

                # Navigate to the URL
                driver.get(url)

                # Wait for the elements in the textual block indicating company names
                WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH,
                         "//div[contains(@class,'t-roman t-sans')]"
                         "//a[@data-test-app-aware-link and contains(@href,'/company/')]"
                        )
                    )
                )

                # Scrape the company names from the page
                company_names = scrape_companies_from_page(driver)

                # Write to CSV
                for name in company_names:
                    writer.writerow([name, ""])  # Email is unknown, leaving it blank

                # (Optional) Sleep between page requests to avoid being flagged
                time.sleep(2)  # Sleep 2 seconds between requests

        print("Scraping completed. Company names have been appended to data_base_501_to_infinity.csv.")

    finally:
        # 6e. Close the driver (important!)
        driver.quit()

# ------------------------------------------------------------------
# 7) EXECUTE IF RUN AS SCRIPT
# ------------------------------------------------------------------
if __name__ == "__main__":
    main()
