"""
Author: Gabriel Isaiah Padus-Carvalion
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

Note -> Change the input_file and output_file variables if needed ;)

"""

####################################################
# SHALL WE START?
####################################################

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
