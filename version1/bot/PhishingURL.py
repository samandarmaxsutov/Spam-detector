import json
import requests
import urllib.parse
import re


def clean_url(url):
    # Remove unwanted characters and extra text
    cleaned_url = re.sub(r'[\\\n\r\s\'"]+', '', url)  # Remove newlines, backslashes, and extra whitespace
    return cleaned_url


def get_links(text):
    # Extract URLs using regex
    pattern = r'https?://[^\s\'"\\()<>]+'
    urls = re.findall(pattern, text)
    clean_urls = [clean_url(url) for url in urls]  # Clean each URL
    return clean_urls


def get_telegram_links(text):
    # Extract Telegram usernames
    pattern = r'@[\w_]+'
    usernames = re.findall(pattern, text)
    urls = [f"https://t.me/{username[1:]}" for username in usernames]  # Convert usernames to URLs
    return urls


def combine_links(text):
    urls = get_links(text)
    telegram_links = get_telegram_links(text)
    urls.extend(telegram_links)  # Add Telegram links to the list of URLs
    return urls


class PhishingCheckerAPI:
    def __init__(self, api_key: str = "R65jPzgUPZDss6hWLS4e5op7OTMOgB7K"):
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


def check_url(url):
    p = PhishingCheckerAPI()
    result = p.malicious_url_scanner_api(url)

    if 'success' in result and result['success'] == True:
        bool_mapping = {
            True: "Ha",
            False: "Yo'q",
            'Unknown': "Noma'lum"
        }

        # Format the result
        formatted_result = (
            f"<b>URL:</b> {url}\n"
            f"<b>Phishing:</b> {bool_mapping.get(result.get('phishing', 'Unknown'))}\n"
            f"<b>Malware:</b> {bool_mapping.get(result.get('malware', 'Unknown'))}\n"
            f"<b>Risk Score:</b> {result.get('risk_score', 'Unknown')}\n"
            f"<b>Suspicious:</b> {bool_mapping.get(result.get('suspicious', 'Unknown'))}\n"
            f"<b>Parking:</b> {bool_mapping.get(result.get('parking', 'Unknown'))}\n"
        )

        return formatted_result
    else:
        return "Failed"
