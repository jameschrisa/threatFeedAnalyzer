# Threat Intelligence Feed Validator

This project provides tools to parse, validate, and maintain a collection of threat intelligence feeds. It includes a JSON configuration of feeds extracted from various sources and a validation script to ensure the feeds are accessible.

## Overview

Threat intelligence feeds are valuable sources of information for cybersecurity teams. However, these feeds can sometimes become unavailable or change their access methods. This project helps maintain an up-to-date list of functional threat intelligence feeds.

### Features

- JSON configuration of 90+ threat intelligence feeds
- Python script to validate feed availability
- Categorization of feeds into RSS feeds and API calls
- Parallel processing for efficient validation
- Detailed error reporting
- Separation of valid and invalid feeds

## Files

- `threat-intel-feeds.json`: Complete list of threat intelligence feeds
- `validate-feeds.py`: Python script to validate feed URLs
- `valid-threat-intel-feeds.json`: Generated file with all valid feeds
- `valid-rss-feeds.json`: Generated file with valid RSS feeds
- `valid-apis.json`: Generated file with valid API calls
- `invalid-threat-intel-feeds.json`: Generated file with invalid feeds and their error messages

## Requirements

- Python 3.6 or higher
- `requests` library

## Installation

### macOS Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/threat-intel-feed-validator.git
   cd threat-intel-feed-validator
   ```

2. Install dependencies using the requirements file:
   ```
   pip3 install -r requirements.txt
   ```

   Note: On macOS, you should use `pip3` to ensure you're using Python 3's package manager.

3. If you encounter any permission issues, you can use:
   ```
   pip3 install --user -r requirements.txt
   ```

## Usage

To validate all feeds and update the JSON files on macOS:

```
python3 validate-feeds.py
```

The script will:
1. Read the original `threat-intel-feeds.json` file
2. Attempt to connect to each feed URL
3. Categorize valid feeds as either RSS feeds or API calls
4. Generate a `valid-threat-intel-feeds.json` with all working feeds
5. Generate a `valid-rss-feeds.json` with working RSS feeds
6. Generate a `valid-apis.json` with working API calls
7. Generate an `invalid-threat-intel-feeds.json` with non-working feeds
8. Display statistics about the validation process

### Output Example

```
Found 85 feeds in the configuration file.
Validating feeds with 10 parallel workers...
---------------------------------------------------
✅ Feed 'Binary Defense IP Banlist' is valid (api)
❌ Feed 'AbuseIPDB' failed: HTTP error 403
✅ Feed 'BOTVRIJ.EU' is valid (api)
...

---------------------------------------------------
Total feeds: 85
Valid feeds: 69
  - RSS feeds: 0
  - API feeds: 69
Invalid feeds: 16

Success: Updated configuration saved to 'valid-threat-intel-feeds.json'
RSS feeds saved to 'valid-rss-feeds.json'
API feeds saved to 'valid-apis.json'
Invalid feeds saved to 'invalid-threat-intel-feeds.json' for reference
```

## Customization

You can modify the script's behavior by changing these constants at the top of the file:

- `REQUEST_TIMEOUT`: Maximum time in seconds to wait for a response (default: 10)
- `MAX_WORKERS`: Number of parallel threads to use (default: 10)

## Using the Feed Data

The validated feed data can be used for:

1. Integration with security information and event management (SIEM) systems
2. Enhancing intrusion detection systems (IDS)
3. Threat hunting and intelligence gathering
4. Security research

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Original feed list compiled from various public threat intelligence sources
- Thanks to all the organizations that maintain these valuable security feeds
