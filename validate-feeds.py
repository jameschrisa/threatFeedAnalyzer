import json
import requests
import sys
from urllib.parse import urlparse
import time
from concurrent.futures import ThreadPoolExecutor
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set timeout for requests (in seconds)
REQUEST_TIMEOUT = 10

# Number of parallel workers
MAX_WORKERS = 10

def is_valid_url(url):
    """
    Check if the URL has a valid structure.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_feed(feed):
    """
    Validate if a feed is accessible.
    Returns a tuple with (feed, is_valid, error_message).
    """
    url = feed["url"]
    name = feed["name"]
    
    # Check if URL has valid format
    if not is_valid_url(url):
        return (feed, False, f"Invalid URL format: {url}")
    
    # Try to access the URL
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        }
        
        # Make a request to the URL
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True, verify=False)
        
        # Check if the response was successful
        if response.status_code < 400:
            print(f"✅ Feed '{name}' is valid")
            return (feed, True, "")
        else:
            error_msg = f"HTTP error {response.status_code}"
            print(f"❌ Feed '{name}' failed: {error_msg}")
            return (feed, False, error_msg)
    
    except requests.exceptions.Timeout:
        error_msg = "Connection timed out"
        print(f"❌ Feed '{name}' failed: {error_msg}")
        return (feed, False, error_msg)

def main():
    """
    Main function to validate feeds and update the JSON file.
    """
    # Read the JSON file
    try:
        with open('threat-intel-feeds.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading the feed configuration file: {e}")
        sys.exit(1)
    
    if 'feeds' not in data:
        print("Error: The JSON file does not contain a 'feeds' key.")
        sys.exit(1)
    
    feeds = data['feeds']
    print(f"Found {len(feeds)} feeds in the configuration file.")
    
    # Validate feeds using ThreadPoolExecutor for parallel processing
    valid_feeds = []
    invalid_feeds = []
    
    print(f"Validating feeds with {MAX_WORKERS} parallel workers...")
    print("---------------------------------------------------")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = list(executor.map(validate_feed, feeds))
    
    # Process results
    for feed, is_valid, error_msg in results:
        if is_valid:
            valid_feeds.append(feed)
        else:
            invalid_feeds.append({
                "feed": feed,
                "error": error_msg
            })
    
    # Print statistics
    print("\n---------------------------------------------------")
    print(f"Total feeds: {len(feeds)}")
    print(f"Valid feeds: {len(valid_feeds)}")
    print(f"Invalid feeds: {len(invalid_feeds)}")
    
    # Write the updated JSON file
    updated_data = {
        "feeds": valid_feeds
    }
    
    try:
        with open('valid-threat-intel-feeds.json', 'w') as f:
            json.dump(updated_data, f, indent=2)
        print(f"\nSuccess: Updated configuration saved to 'valid-threat-intel-feeds.json'")
    except Exception as e:
        print(f"\nError writing the updated configuration file: {e}")
    
    # Write the invalid feeds to a separate file for reference
    if invalid_feeds:
        try:
            with open('invalid-threat-intel-feeds.json', 'w') as f:
                json.dump({"invalid_feeds": invalid_feeds}, f, indent=2)
            print(f"Invalid feeds saved to 'invalid-threat-intel-feeds.json' for reference")
        except Exception as e:
            print(f"Error writing the invalid feeds file: {e}")

if __name__ == "__main__":
    main()
    
    except requests.exceptions.SSLError:
        error_msg = "SSL Error"
        print(f"❌ Feed '{name}' failed: {error_msg}")
        return (feed, False, error_msg)
    
    except requests.exceptions.ConnectionError:
        error_msg = "Connection error"
        print(f"❌ Feed '{name}' failed: {error_msg}")
        return (feed, False, error_msg)
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Feed '{name}' failed: {error_msg}")
        return (feed, False, error_msg)