import joblib
import requests
from bs4 import BeautifulSoup
import numpy as np
from urllib.parse import urlparse
import pandas as pd
import magic
import math

# Load the trained Random Forest model
model = joblib.load('./trained_model/random_forest_model.pkl')

# Load the CSV dataset to get mean and mode values
df = pd.read_csv('./datasets/df_clear.csv')

# Get statistical values from the dataset to use as placeholders
mean_values = df.mean()
mode_values = df.mode().iloc[0]  # Get the first row of mode (most frequent values)

# Function to ensure the URL has a scheme (https or http)
def add_scheme_if_missing(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        # If no scheme is provided, default to https
        return 'https://' + url
    return url

# Calculate the entropy of a file
def calculate_entropy(data):
    if len(data) == 0:
        return 0
    byte_counts = np.bincount(np.frombuffer(data, dtype=np.uint8), minlength=256)
    probabilities = byte_counts / len(data)
    entropy = -np.sum([p * math.log2(p) for p in probabilities if p > 0])
    return entropy

# Function to check if the content is a file and get its MIME type
def is_file_content(response):
    mime = magic.Magic(mime=True)  # Initialize magic for MIME detection
    content_type = mime.from_buffer(response.content)
    return content_type

# Function to extract file-related features (similar to how we extract website features)
def extract_file_features(content):
    try:
        # Calculate file-specific features
        file_size_kb = len(content) // 1024  # Size in KB
        entropy = calculate_entropy(content)  # Entropy of the file
        suspicious_strings = int(any(keyword in content.lower() for keyword in [b'bitcoin', b'crypto', b'wallet', b'encrypt']))  # Suspicious strings

        # Collect file-related features
        features = [
            mode_values['Machine'],                    # Feature 1: Placeholder for machine info
            mean_values['DebugSize'],                  # Feature 2: Placeholder for DebugSize (from dataset)
            file_size_kb,                              # Feature 3: File size in KB
            entropy,                                   # Feature 4: Entropy of the file
            mean_values['MajorOSVersion'],             # Feature 5: Placeholder for OS version
            suspicious_strings,                        # Feature 6: Suspicious strings in file
            mean_values['MajorLinkerVersion'],         # Feature 7: Placeholder for linker version
            mean_values['MinorLinkerVersion'],         # Feature 8: Placeholder for linker version
            mean_values['ExportRVA'],                  # Feature 9: Placeholder
            mean_values['ExportSize'],                 # Feature 10: Placeholder
            mean_values['IatVRA'],                     # Feature 11: Placeholder
            1 if content.startswith(b'MZ') else 0,     # Feature 12: Check for 'MZ' header (common in PE files)
            entropy > 7.5,                             # Feature 13: Entropy threshold for highly random files
            file_size_kb,                              # Feature 14: File size repeated
        ]

        # Print debug information about features
        print(f"Extracted file features: {features}")

        # Ensure we only return 15 features
        while len(features) < 15:
            features.append(0)

        return np.array(features)

    except Exception as e:
        print(f"Error extracting file features: {e}")
        return None

# Function to extract website features for the ransomware model
def extract_website_features(url):
    try:
        url = add_scheme_if_missing(url)  # Ensure the URL has the scheme
        # Fetch the website content
        response = requests.get(url, timeout=5)

        # Check if the URL points to a file or webpage
        content_type = is_file_content(response)

        if content_type.startswith('application/'):  # Likely a file (e.g., exe, dll)
            return extract_file_features(response.content)
        else:
            # Treat it as a webpage and scrape content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Check if the site is using HTTPS
            ssl_status = 1 if urlparse(url).scheme == 'https' else 0

            # Get the domain name and its length
            domain_name = urlparse(url).netloc
            domain_length = len(domain_name)

            # Collect features from the webpage
            features = [
                mode_values['Machine'],                      # Feature 1
                mean_values['DebugSize'],                    # Feature 2
                len(soup.find_all('div')),                   # Feature 3
                len(soup.find_all(['link', 'script', 'img'])),  # Feature 4
                mode_values['MajorOSVersion'],               # Feature 5
                int(any(keyword in soup.get_text().lower() for keyword in ['bitcoin', 'crypto', 'wallet'])),  # Feature 6
                len(response.content) // 1024,               # Feature 7 (size in KB)
                mean_values['MajorLinkerVersion'],           # Feature 8
                mean_values['MinorLinkerVersion'],           # Feature 9
                mean_values['ExportRVA'],                    # Feature 10
                mean_values['ExportSize'],                   # Feature 11
                mean_values['IatVRA'],                       # Feature 12
                ssl_status,                                  # Feature 13: SSL certificate                                 
                domain_length,                               # Feature 14: Length of the domain name
            ]

            # Ensure we only return 15 features
            while len(features) < 15:
                features.append(0)

            # Print extracted website features
            print(f"Extracted website features: {features}")

            return np.array(features)

    except Exception as e:
        print(f"Error extracting features from website: {e}")
        return None

# Function to check if a website or file has ransomware using the model's prediction
def check_ransomware(url):
    features = extract_website_features(url)

    if features is not None:
        # Reshape features for model input
        features = features.reshape(1, -1)  # Reshape to 2D array for prediction

        # Make a prediction using the model
        prediction = model.predict(features)
        prediction_prob = model.predict_proba(features)

        # Print detailed probability insights
        print(f"Prediction probability for {url}: {prediction_prob}")

        # Adjust threshold to classify ransomware based on the second column (ransomware probability)
        if prediction[0] == 1:  # Assuming '1' indicates ransomware
            print(f"Website {url} has ransomware.")
        else:
            print(f"Website {url} is safe.")
    else:
        print(f"Failed to check website {url}.")

# Example usage
website_url = "https://www.youtube.com/"  # Replace with the actual website URL you want to check
check_ransomware(website_url)
