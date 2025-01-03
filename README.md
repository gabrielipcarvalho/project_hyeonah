Certainly! Below is a comprehensive `README.md` file for your project, **Project Hyeonah**, formatted using Markdown. You can copy and paste this content directly into your `README.md` file.

---

# Project Hyeonah

![Project Hyeonah Logo](path/to/your/logo.png) _(Optional: Add a logo or relevant image)_

## Table of Contents

-   [Project Hyeonah](#project-hyeonah)
    -   [Table of Contents](#table-of-contents)
    -   [Description](#description)
    -   [Features](#features)
    -   [Project Structure](#project-structure)
    -   [Prerequisites](#prerequisites)
    -   [Installation](#installation)
    -   [Configuration](#configuration)
    -   [Usage](#usage)
        -   [Web Scraping Script](#web-scraping-script)
        -   [CSV Processing Script](#csv-processing-script)
    -   [Dependencies](#dependencies)
    -   [Contributing](#contributing)
    -   [License](#license)
    -   [Author](#author)

## Description

**Project Hyeonah** automates the process of scraping company names from LinkedIn based on specific search parameters and processes the scraped data to ensure it adheres to a standardized CSV format. This project comprises two main scripts:

1. **Web Scraping Script (`web_scraping.py`)**: Automates logging into LinkedIn, navigating through company search result pages, scraping company names, and appending them to a CSV file.
2. **CSV Processing Script (`process_csv.py`)**: Cleans the scraped CSV data by removing trailing whitespaces and ensuring each row ends with a comma, indicating an empty second column.

## Features

-   **Automated LinkedIn Scraping**: Logs into LinkedIn and navigates through multiple search result pages to scrape company names.
-   **Data Cleaning**: Processes the scraped data to remove inconsistencies and prepare it for further analysis or usage.
-   **Environment Variable Management**: Uses environment variables to securely manage LinkedIn credentials.
-   **Headless Browser Automation**: Utilizes Selenium WebDriver in headless mode to perform scraping without opening a browser window.
-   **CSV Management**: Handles reading from and writing to CSV files efficiently.

## Project Structure

```
.
├── data
│   └── db
│       ├── data_base_11_to_500.csv
│       └── data_base_11_to_500_modified.csv
├── src
│   ├── process_csv.py
│   └── web_scraping.py
├── .gitignore
├── README.md
└── requirements.txt
```

-   **data/db/**: Contains the original and processed CSV files.
    -   `data_base_11_to_500.csv`: Original CSV file with scraped company names.
    -   `data_base_11_to_500_modified.csv`: Processed CSV file with cleaned data.
-   **src/**: Contains the Python scripts.
    -   `web_scraping.py`: Script for scraping company names from LinkedIn.
    -   `process_csv.py`: Script for cleaning and processing the CSV file.
-   **.gitignore**: Specifies files and directories to be ignored by Git.
-   **README.md**: Documentation for the project.
-   **requirements.txt**: Lists the Python dependencies required for the project.

## Prerequisites

-   **Python 3.7 or higher**
-   **Git**
-   **LinkedIn Account**: Valid credentials to access LinkedIn for scraping.
-   **GitHub Account**: To host the repository and manage version control.

## Installation

1. **Clone the Repository**

    ```bash
    git clone git@github.com:gabrielipcarvalho/project_hyeonah.git
    cd project_hyeonah
    ```

2. **Set Up a Virtual Environment (Recommended)**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. **Create a `.env` File**

    In the root directory of your project, create a `.env` file to store your LinkedIn credentials securely.

    ```bash
    touch .env
    ```

    **Add the following to the `.env` file:**

    ```env
    LINKEDIN_EMAIL=your_linkedin_email@example.com
    LINKEDIN_PASSWORD=your_secure_password
    ```

    **Note:** Ensure that the `.env` file is included in your `.gitignore` to prevent sensitive information from being pushed to GitHub.

## Usage

### Web Scraping Script

**Script:** `src/web_scraping.py`

This script logs into LinkedIn, navigates through company search result pages based on predefined search parameters, scrapes company names, and appends them to a CSV file.

**Steps:**

1. **Ensure Dependencies are Installed**

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the Web Scraping Script**

    ```bash
    python src/web_scraping.py
    ```

**Description of `web_scraping.py`:**

```python
"""
Author: Gabriel Isaiah Padus-Carvalho
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
- The file paths are previously defined; if you ever change the file paths, remember to update them here too.

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
    "&companySize=%5B%22C%22%2C%22D%22%2C%22E%22%5D"
    "&industryCompanyVertical=%5B%2296%22%2C%221594%22%2C%226%22%2C%224%22%5D"
    "&keywords=software"
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

    # Find all 'a' tags with the specific class that encloses company names
    anchor_tags = driver.find_elements(By.CLASS_NAME, "OuPhnhXhvqFqqqKGsGzJvJbbQzqQqoBaHlDLUuWA ")

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
        csv_path = "../data/db/data_base_11_to_500.csv"  # Adjust if your relative path is different
        with open(csv_path, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Assumes the header row ["Name", "Email"] is already in place.

            # 6d. Scrape the pages
            for page_num in range(1, 83):  # Pages 1 through 82
                url = SEARCH_BASE_URL.format(page_num=page_num)
                print(f"Scraping page {page_num} -> {url}")

                # Navigate to the URL
                driver.get(url)

                # Wait until the company listings are loaded
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "OuPhnhXhvqFqqqKGsGzJvJbbQzqQqoBaHlDLUuWA ")))

                # Scrape the company names from the page
                company_names = scrape_companies_from_page(driver)

                # Write to CSV
                for name in company_names:
                    writer.writerow([name, ""])  # Email is unknown, leaving it blank

                # (Optional) Sleep between page requests to avoid being flagged
                time.sleep(2)  # Sleep 2 seconds between requests

        print("Scraping completed. Company names have been appended to data_base_11_to_500.csv.")

    finally:
        # 6e. Close the driver (important!)
        driver.quit()

# ------------------------------------------------------------------
# 7) EXECUTE IF RUN AS SCRIPT
# ------------------------------------------------------------------
if __name__ == "__main__":
    main()
```

### CSV Processing Script

**Script:** `src/process_csv.py`

This script processes the scraped CSV file by removing trailing whitespaces from each cell and ensuring each row ends with a comma, indicating an empty second column.

**Steps:**

1. **Ensure Dependencies are Installed**

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the CSV Processing Script**

    ```bash
    python src/process_csv.py
    ```

**Description of `process_csv.py`:**

```python
"""
Author: Gabriel Isaiah Padus-Carvalho
Date: 03-01-2025

Description:
This script processes a CSV file by removing any trailing whitespace from each cell in every row.
It then ensures that each row ends with a comma, representing an empty second column,
preserving the CSV structure. The modified data is written to a new output CSV file.

The script performs the following steps:
1. Reads the input CSV file ('data_base_11_to_500.csv') located in the '../data/db' directory.
2. Strips trailing whitespace from each cell in every row.
3. Adds a comma at the end of each row by appending an empty string ('') as the second column.
4. Writes the modified rows to a new CSV file ('data_base_11_to_500_modified.csv').

Note: Change the input_file and output_file variables if needed ;)
"""

import csv

# Define the path to the CSV file
input_file = '../data/db/data_base_11_to_500.csv'
output_file = '../data/db/data_base_11_to_500_modified.csv'

# Open the input CSV file for reading
with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    # Create a CSV reader object
    reader = csv.reader(infile)

    # Open the output file to write the modified rows
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)

        # Iterate through each row in the input file
        for row in reader:
            # Remove trailing whitespace from each cell
            row = [cell.rstrip() for cell in row]

            # Ensure that the row ends with an empty value for the second column
            # This will place a comma after the first column in each row
            row.append('')  # Add empty second column

            # Write the modified row to the output file
            writer.writerow(row)

print(f"File processed successfully. The modified file is saved as '{output_file}'.")
```

## Dependencies

The project relies on the following Python libraries:

-   [Selenium](https://pypi.org/project/selenium/): Browser automation tool.
-   [webdriver-manager](https://pypi.org/project/webdriver-manager/): Manages browser drivers for Selenium.
-   [python-dotenv](https://pypi.org/project/python-dotenv/): Loads environment variables from a `.env` file.

All dependencies are listed in the `requirements.txt` file. To install them, run:

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```
selenium==4.10.0
webdriver-manager==3.8.6
python-dotenv==1.0.0
```

_(Ensure that the versions match the ones you have installed. You can update them accordingly.)_

## Author

**Gabriel Isaiah Padus-Carvalho**

-   [GitHub](https://github.com/gabrielipcarvalho)
