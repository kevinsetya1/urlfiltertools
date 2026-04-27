import pandas as pd
import tldextract
from datetime import datetime
from urllib.parse import urlparse
import re

def convert_to_wildcard(url):
    print(f"Processing URL: {url}")  # Logging for debugging

    # Add dummy scheme if not present
    if not url.startswith(('http://', 'https://', 'ftp://')):
        url = 'http://' + url

    # Parse URL to handle cases with port numbers
    parsed_url = urlparse(url)
    
    # Check if this is an IP address
    ip_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    is_ip = re.match(ip_pattern, parsed_url.hostname)
    
    if is_ip:
        # If this is an IP address
        result = f"{parsed_url.hostname}"
        if parsed_url.port:
            result += f":{parsed_url.port}"
    else:
        # If this is a domain
        extracted = tldextract.extract(parsed_url.netloc)
        main_domain = f"{extracted.domain}.{extracted.suffix}"
        if parsed_url.port:
            main_domain += f":{parsed_url.port}"
        
        if extracted.subdomain:
            result = f"*.{main_domain}"
        else:
            result = main_domain

    # Clean up the result
    result = result.strip().rstrip('.:')
    
    # Add trailing slash if not present
    if not result.endswith('/'):
        result += '/'
    
    print(f"Converted result: {result}")  # Logging for debugging

    # Validate format using regex
    ip_port_pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?/$'
    domain_pattern = r'^(\*\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(:\d+)?/$'
    
    if re.match(ip_port_pattern, result) or re.match(domain_pattern, result):
        print(f"Valid format: {result}")  # Logging for debugging
        return result
    else:
        print(f"Warning: Invalid format detected: {result}")  # Logging for debugging
        # Return the result even if format is invalid
        return result

def write_to_file(file, message):
    file.write(message + "\n")

# Read list of URLs from Excel file
file_path = 'list_urls.xlsx'  # Replace with your Excel file path
try:
    df = pd.read_excel(file_path)
    read_success = f"Successfully read file: {file_path}"
    row_count = f"Total rows of data: {len(df)}"
    print(read_success)
    print(row_count)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    exit()
except Exception as e:
    print(f"An error occurred while reading the file: {e}")
    exit()

# Assuming URLs are in the first column; change column name if needed
url_list = df.iloc[:, 0].tolist()
url_count = f"Total URLs read: {len(url_list)}"
print(url_count)

# Convert all URLs in the list using the function
wildcard_list = []
for url in url_list:
    wildcard = convert_to_wildcard(url)
    if wildcard and wildcard not in wildcard_list:  # Ensure no duplicates
        wildcard_list.append(wildcard)

wildcard_count = f"Total wildcards generated: {len(wildcard_list)}"
print(wildcard_count)

# Create a dictionary to group URLs by their wildcard result
grouped_results = {}

for url in url_list:
    result = convert_to_wildcard(url)
    if result not in grouped_results:
        grouped_results[result] = []
    grouped_results[result].append(url)

# Write output and log to file
try:
    with open('wildcard_urls.txt', 'w') as file:
        # Write initial information
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_to_file(file, f"Process Log ({timestamp}):")
        write_to_file(file, read_success)
        write_to_file(file, row_count)
        write_to_file(file, url_count)
        write_to_file(file, wildcard_count)
        write_to_file(file, "\nWildcard URL List:")
        
        # Write sorted wildcard URLs
        for wildcard in sorted(wildcard_list):
            write_to_file(file, wildcard)
        
        # Write separator line
        separator = "\n" + "-"*50 + "\n"
        write_to_file(file, separator)
        
        # Write grouped conversion log
        write_to_file(file, "Detailed Conversion Log (Grouped):")
        for wildcard in sorted(grouped_results.keys()):
            write_to_file(file, f"\n{wildcard}:")
            for url in sorted(grouped_results[wildcard]):
                write_to_file(file, f"  {url}")
        
    print("Output and conversion log have been saved to 'wildcard_urls.txt'.")
    
    # Display conversion results in terminal
    print("\nConversion results (Grouped):")
    for wildcard in sorted(grouped_results.keys()):
        print(f"\n{wildcard}:")
        for url in sorted(grouped_results[wildcard]):
            print(f"  {url}")

except Exception as e:
    error_message = f"An error occurred while writing the file: {e}"
    print(error_message)
