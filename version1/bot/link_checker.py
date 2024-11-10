import re

# The text from which you want to extract the link
text = """
Writing task 1 qanday boshlanadi?

🧐 Writing task 1 ni boshlashda qanday so'zlardan foydalanmasligingiz kerak ekanini bilasizmi?

😉 Yuqoridagi videoni ko'ring va task 1 ni boshlashda duch keladigan qiyinchiliklardan qutiling!

📌 Videoni IELTS o'qiyotgan tanishlaringiz bilan ham ulashishni unutmang!

📍Manzil: Yunusobod tumani A. Temur ko'chasi 129B
📍Mo'ljal: Shahriston metro

Bizni ijtimoiy tarmoqlarda kuzating👇

Telegram (https://t.me/Registan_shahriston) | Instagram (https://www.instagram.com/registan_shahriston) | You tube (https://youtube.com/@Registan_Shahriston?si=aB0K9CNIDIuDKaYa) | Manzilimiz (https://www.google.com/maps/place/Registon+LC/@41.355422,69.2882519,115m/data=!3m1!1e3!4m5!3m4!1s0x38aef3c9a1d3070f:0xfa8ef226ff2f1f88!8m2!3d41.3555466!4d69.28798)
"""

# Regular expression to find URLs, avoiding trailing parenthesis
pattern = r'https?://[^\s)]+'

# Find all matching URLs in the text
links = re.findall(pattern, text)

# Print the extracted link(s)
for link in links:
    print(link)
