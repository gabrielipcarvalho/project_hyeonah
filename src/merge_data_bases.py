import os
import csv

def merge_csv_files(input_dir, output_file):
    header = ["NAME", "EMAIL"]  # Specified header

    with open(output_file, mode='w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the specified header

        for filename in os.listdir(input_dir):
            file_path = os.path.join(input_dir, filename)
            # Skip the output file to prevent infinite loop
            if filename.endswith('.csv') and file_path != output_file:
                with open(file_path, mode='r') as infile:
                    reader = csv.reader(infile)
                    next(reader)  # Skip the header of the current CSV file
                    for row in reader:
                        writer.writerow(row)

    print(f"All CSV files in '{input_dir}' have been merged into '{output_file}'.")
    return

# usage:
merge_csv_files("../data/db", "../data/db/complete_data_base.csv")
