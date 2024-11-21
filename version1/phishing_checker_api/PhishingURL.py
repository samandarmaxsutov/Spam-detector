import json
import requests
import urllib.parse


class PhishingCheckerAPI:
    def __init__(self, api_key: str):
        self.key = api_key

    def malicious_url_scanner_api(self, url: str, vars: dict = {}) -> dict:
        encoded_url = urllib.parse.quote_plus(url)
        api_url = f'https://www.ipqualityscore.com/api/json/url/{self.key}/{encoded_url}'
        try:
            response = requests.get(api_url, params=vars)
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json()  # Convert response to JSON
            return result
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return {}
        except json.JSONDecodeError:
            print("Error decoding JSON response")
            return {}


if __name__ == "__main__":
    # URL to scan
    URL = 'https://www.kunss.uz'

    # Adjustable strictness level from 0 to 2
    strictness = 0

    # Custom fields
    additional_params = {
        'strictness': strictness
    }

    # Initialize PhishingCheckerAPI with API key
    API_KEY = ''  
    phishing_checker = PhishingCheckerAPI(API_KEY)

    # Get the result from the API
    result = phishing_checker.malicious_url_scanner_api(URL, additional_params)

    # Print the result
    if result:
        if result.get('success'):
            print(f"Success: {result.get('message')}")
        else:
            print(f"Failed to check URL: {result.get('message', 'No message available')}")
    else:
        print("No result returned from the API")
