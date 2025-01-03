# Project Hyeonah

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

## Author

**Gabriel Isaiah Padus-Carvalho**

-   [GitHub](https://github.com/gabrielipcarvalho)
