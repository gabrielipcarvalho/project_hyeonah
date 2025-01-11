import openai
import csv
import time

# Set up your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Input and output file paths
input_csv = "companies.csv"  # Replace with your actual CSV file path
output_csv = "company_emails.csv"

# Function to query OpenAI for email addresses
def get_company_email(company_name):
    prompt = (
        f"You are tasked with finding the precise and exact contact email for the company '{company_name}' located in Brisbane, Australia. "
    	"Use all resources available to you and try as hard as possible to find a real, existing email. "
    	"The email must be accurate and real, not made up or fabricated. "
    	"If you cannot find a precise email, return exactly the phrase 'email not found'. "
    	"Your response must only contain either the email address or 'email not found' without any other strings, explanations, or details."
	)
    
    try:
        response = openai.ChatCompletion.create(
            model="GPT-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.2
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error fetching email for {company_name}: {e}")
        return "Error"

# Open the CSV file and process each company
with open(input_csv, newline='', encoding='utf-8') as infile, open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    # Write header for the output CSV
    writer.writerow(["Company Name", "Email Address"])
    
    # Skip the header row if present
    next(reader, None)
    
    for row in reader:
        company_name = row[0]
        email = get_company_email(company_name)
        writer.writerow([company_name, email])
        print(f"Processed: {company_name} -> {email}")
        
        # Rate limiting to avoid hitting API limits
        time.sleep(1)  # Adjust sleep time as needed
