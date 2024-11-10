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

# Example usage
a = """
💻 Sizni hamyonbop noutbuklar kutmoqda...

🧑‍💻 Hozirgi kunda ko'pchilik noutbuk uchun bozorlarga bormay, onlayn sotib olishni afzal ko'rmoqda. Sababi, ham vaqt ham pul tejaladi. Telegramdagi @noutbukcom kanali ham siz kabi xaridorlarga "shokolad" narxlarda noutbuklar tayyorlab qo'ygan.

🚚 Siz o'tirgan joyingizgacha yetkazib berish xizmati ham bor!

😍 Aytgandek bizning kanal nomidan aloqaga chiqsangiz "zo'rkuuu" deydigan chegirmalar qilib berishadi

👉 Kanalga marhamat: @noutbukcom

Check this out: https://kun.uz/46038422\\n\\nKun.uz
Also visit: https://t.me/kunuz'
"""

links = combine_links(a)
print("Extracted URLs:", links)
