import logging
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters
from version1.spam_detector.real_time_spam_detector import RealTimeSpamDetector
from version1.bot.users_data import User, UserMessages, UserFeedbacks
from version1.bot.PhishingURL import combine_links, check_url

TOKEN = "TOKEN"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

real_time_spam_detector = RealTimeSpamDetector()
last_message = ""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    print(user.id)
    existing_user = User.get_user_by_telegram_id(user.id)

    if existing_user is None:
        # Create buttons for Yes and No
        keyboard = [
            [InlineKeyboardButton("Ha ✅", callback_data='save_yes')],
            [InlineKeyboardButton("Yo'q ❌", callback_data='save_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_html(text="""
👋 Salom! {user.name}

Men ai xabarlarini aniqlashda yordam beruvchi botman. Quyidagi komandalar mavjud:

1️⃣ **/help**: Botning imkoniyatlari haqida ma'lumot olish.
2️⃣ **/info**: Phishing xabarlarini aniqlash haqida qo‘shimcha ma’lumot olish.
3️⃣ **/tips**: Phishing hujumlariga qarshi himoyalanish bo‘yicha foydali maslahatlar olish.
4️⃣ **/check [matn yoki link]**: Shubhali matn yoki linkni tekshirish.
5️⃣ **/report**: Shubhali ai xabarini yoki linkni hisobot sifatida yuboring.

Yordamga muhtoj bo‘lsangiz, **/help** komandasini ishlating.
        """,
                                        parse_mode="HTML",
                                        reply_markup=reply_markup
                                        )
    else:
        await update.message.reply_text(f"Xush kelibsiz , {user.name}!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send help message with formatted text
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
📚 **Yordam bo‘limi**

Salom! Botimiz sizga ai xabarlardan himoyalanishda yordam beradi. Quyidagi komandalar mavjud:

1️⃣ **/start**: Bot bilan muloqotni boshlash va asosiy imkoniyatlarni ko‘rish.
2️⃣ **/check [matn yoki link]**: Shubhali matn yoki linkni tekshirish.
3️⃣ **/tips**: Phishing hujumlariga qarshi himoyalanish bo‘yicha foydali maslahatlar olish.
4️⃣ **/report**: Shubhali ai xabarini yoki linkni hisobot sifatida yuboring.
5️⃣ **/settings**: Botning sozlamalarini ko‘rish va o‘zgartirish.
Agar sizda boshqa savollar bo‘lsa, bizga murojaat qiling yoki yordam uchun bu komandalarni foydalaning.

🔒 **Hushyor bo‘ling va xavfsiz bo‘ling!**
        """,
        parse_mode="HTML"
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Here, you might collect and report the ai content.
    # For demonstration, we'll just send a placeholder message.

    reported_content = " ".join(context.args)
    # Perform reporting here...

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"📝 **Shubhali kontent hisobot qilingan:**\n\n{reported_content}\n\nBiz sizning hisobotingizni ko‘rib chiqamiz. Rahmat!",
        parse_mode="HTML"
    )


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Here, you might process the text or link to check for ai.
    # For demonstration, we'll just send a placeholder message.
    text_to_check = " ".join(context.args)
    # Perform ai check here...

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"🔍 **Shubhali matn yoki linkni tekshirayotganingiz:**\n\n{text_to_check}\n\nIltimos, matn yoki linkni tahlil qilish uchun ushbu funksiyani amalga oshiring.",
        parse_mode="HTML"
    )


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allow the user to change their message saving preference."""
    user = update.effective_user
    existing_user = User.get_user_by_telegram_id(user.id)

    if existing_user is not None:
        # Create buttons for changing the setting
        current_setting = "Ha ✅" if existing_user.save_message else "Yo'q ❌"
        keyboard = [
            [InlineKeyboardButton("Ha ✅", callback_data='save_yes')],
            [InlineKeyboardButton("Yo'q ❌", callback_data='save_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_html(
            text=f"Sizning hozirgi sozlamalaringiz:\n {current_setting}.\nXabarlaringiz saqlab qolinsinmi?",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text("Siz hali ro'yxatdan o'tmagansiz. Iltimos, /start buyrug'idan foydalaning.")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the video file path or URL
    video_path = './video.mp4'  # Or provide a URL instead

    # Send the video with a caption
    await context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=video_path,
        caption="""
📌 **Phishing haqida ma'lumot:**

Phishing – bu kiberhujum turidir, unda xakerlar foydalanuvchilarni aldash orqali shaxsiy ma'lumotlarni (masalan, parol, karta ma’lumotlari, login) qo‘lga kiritishga harakat qiladi. 

Phishing hujumlari odatda:
- 📧 Elektron pochta
- 💬 Messenjerlar
- 🌐 Soxta veb-saytlar

orqali amalga oshiriladi. 

Hujumchilar foydalanuvchini ishonchli manba (bank, ijtimoiy tarmoq, davlat tashkiloti) vakili sifatida ko‘rsatib, ularning maxfiy ma'lumotlarini so‘rashadi.

🔒 **Hushyor bo‘ling va shaxsiy ma'lumotlaringizni himoya qiling!**
        """,
        parse_mode="HTML"
    )


async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Send the video with a caption
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
🎯 <b>Phishing hujumlaridan himoyalanish bo‘yicha 9 ta foydali maslahat:</b>

1️⃣ <b>Linklarni diqqat bilan tekshiring:</b> Shubhali linklarga kirmang. Faqat rasmiy manbalar orqali saytlarga kiring.

2️⃣ <b>Shubhali xabarlarga e’tibor bermang:</b> Tezkor harakat qilish yoki shaxsiy ma’lumotlar so‘ralayotgan xabarlarga aldanmang.

3️⃣ <b>Yuboruvchini tekshiring:</b> Elektron pochta yoki SMS’larda yuboruvchining manzilini sinchiklab ko‘rib chiqing.

4️⃣ <b>Imlo va grammatik xatolarga e’tibor bering:</b> Phishing xabarlarida ko‘pincha xatolar ko‘p uchraydi.

5️⃣ <b>Shaxsiy ma’lumotlarni baham ko‘rmang:</b> Hech qachon parol, bank kartasi raqami yoki PIN kod kabi maxfiy ma’lumotlarni bermang.

6️⃣ <b>Ikki faktorli autentifikatsiyani yoqing:</b> Qo‘shimcha xavfsizlik uchun 2FA funksiyasidan foydalaning.

7️⃣ <b>Antivirusni yangilang:</b> Qurilmangizda yangilangan antivirus dasturi bo‘lsin.

8️⃣ <b>Xabarlarni tasdiqlang:</b> Shubhali xabarlar haqida rasmiy manbalardan ma’lumot oling.

9️⃣ <b>Soxta ilovalardan ehtiyot bo‘ling:</b> Faqat ishonchli manbalardan ilovalarni yuklab oling.

🔒 <b>Hushyor bo‘ling va o‘zingizni ai hujumlaridan himoya qiling!</b>
        """,
        parse_mode="HTML"
    )


async def handle_save_preference(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the user's response to the save message preference."""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    save_message = query.data == 'save_yes'

    # Update the user's preference in the database
    existing_user = User.get_user_by_telegram_id(user.id)

    if existing_user:
        existing_user.save_message = save_message
        existing_user.update()
    else:
        # If the user is not found (which should not happen), create a new entry
        new_user = User(telegram_id=user.id, save_message=save_message)
        new_user.add_user()

    await query.edit_message_text(parse_mode='HTML',
                                  text=f"Sizning tanlovingiz qabul qilindi:\n {'<b>Xabarlarni saqlab qolish yoqilgan ✅.</b>' if save_message else '<b>Xabarlarni saqlab qolish o‘chirilgan ❌</b>'}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages."""
    try:
        global last_message
        print(update.message)
        text = update.message.text
        a = str(update.message)
        # Extract URLs from the text
        urls = combine_links(a)
        logger.info(f"Extracted URLs: {urls}")

        results = []
        # for url in urls:
        #     result = check_url(url)
        #     results.append(result + "\n")
        #
        # # Format the response with the phishing results
        # response = '\n'.join(results)
        # if response:
        #     await update.message.reply_text(f"<b>Phishing URL Natijalari:</b>\n\n{response}",
        #                                     parse_mode='HTML')
        # logger.info(f"Received text message: {text}")
        last_message = text
        # Get the prediction and confidence from the spam detector
        prediction, confidence = await real_time_spam_detector.predict(text)

        user = update.effective_user
        # Fetch the user from the database
        current_user = User.get_user_by_telegram_id(user.id)

        if current_user:
            # Save the message if the user has opted to do so
            if current_user.save_message:
                is_spam = prediction == 'Spam xabar ❌'
                message = UserMessages(text=text, spam=is_spam, user_id=user.id)
                message.add_message()

        # Format the response with HTML
        response = (
            f"<b>Prediction:</b> {prediction}\n"
            f"<b>Spam xabar bo'lish ehtimoligi:</b> {confidence['spam']:.2f}% 📊"
        )
        print(user.name + "\n" + response)
        # Create feedback buttons
        keyboard = [
            [InlineKeyboardButton("👍 Ha", callback_data='feedback_yes')],
            [InlineKeyboardButton("👎 Yo'q", callback_data='feedback_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the response with the feedback buttons
        await update.message.reply_text(response, parse_mode="HTML", reply_to_message_id=update.message.message_id,
                                        reply_markup=reply_markup)

        # Forward the message to the channel and delete the original if spam probability is greater than 90%
        if confidence['spam'] > 90:
            channel_username = '@spam_messages_uz'  # Replace with your channel's username or ID
            await context.bot.forward_message(chat_id=channel_username, from_chat_id=update.message.chat_id,
                                              message_id=update.message.message_id)

            # Notify user about deletion and provide channel link
            reason_message = (
                "<b>Sizning xabaringiz spam deb topildi va o'chirildi.</b> \n"
                "<i>Agar spam xabar bo'lish ehtimoligi 90% dan yuqori bo'lsa xabar o'chirib yuboriladi.</i>\n"
                "Xabarlarni ko'rish uchun kanalga qarang:\n"
                f"<a href='https://t.me/{channel_username[1:]}'>{channel_username}</a>"
            )

            await update.message.reply_text(reason_message, parse_mode="HTML")

            # Delete the original message
            await update.message.delete()

    except Exception as e:
        logger.error(f"Xatolik: {e}")
        await update.message.reply_text(f"Xatolik: {e}")


async def handle_caption(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular caption messages."""
    try:
        global last_message
        text = update.message.caption
        a = str(update.message)
        # Extract URLs from the text
        urls = combine_links(a)
        logger.info(f"Extracted URLs: {urls}")

        # results = []
        # for url in urls:
        #     result = check_url(url)
        #     results.append(result + "\n")
        #
        # # Format the response with the phishing results
        # response = '\n'.join(results)
        # if response:
        #     await update.message.reply_text(f"<b>Phishing URL Natijalari:</b>\n\n{response}",
        #                                     parse_mode='HTML')

        logger.info(f"Received caption: {text}")
        last_message = text
        # Get the prediction and confidence from the spam detector
        prediction, confidence = await real_time_spam_detector.predict(text)

        user = update.effective_user
        # Fetch the user from the database
        current_user = User.get_user_by_telegram_id(user.id)

        if current_user:
            # Save the message if the user has opted to do so
            if current_user.save_message:
                is_spam = prediction == 'Spam xabar ❌'
                message = UserMessages(text=text, spam=is_spam, user_id=user.id)
                message.add_message()

        # Format the response with HTML
        response = (
            f"<b>Prediction:</b> {prediction}\n"
            f"<b>Spam xabar bo'lish ehtimoligi:</b> {confidence['spam']:.2f}% 📊"
        )
        print(user.name + "\n" + response)
        # Create feedback buttons
        keyboard = [
            [InlineKeyboardButton("👍 Ha", callback_data='feedback_yes')],
            [InlineKeyboardButton("👎 Yo'q", callback_data='feedback_no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the response with the feedback buttons
        await update.message.reply_text(response, parse_mode="HTML", reply_to_message_id=update.message.message_id,
                                        reply_markup=reply_markup)

        # Forward the message to the channel and delete the original if spam probability is greater than 90%
        if confidence['spam'] > 90:
            channel_username = '@spam_messages_uz'  # Replace with your channel's username or ID
            await context.bot.forward_message(chat_id=channel_username, from_chat_id=update.message.chat_id,
                                              message_id=update.message.message_id)

            # Notify user about deletion and provide channel link
            reason_message = (
                "<b>Sizning xabaringiz spam deb topildi va o'chirildi.</b> \n"
                "<i>Agar spam xabar bo'lish ehtimoligi 90% dan yuqori bo'lsa xabar o'chirib yuboriladi.</i>\n"
                "Xabarlarni ko'rish uchun kanalga qarang:\n"
                f"<a href='https://t.me/{channel_username[1:]}'>{channel_username}</a>"
            )

            await update.message.reply_text(reason_message, parse_mode="HTML")

            # Delete the original message
            await update.message.delete()

    except Exception as e:
        logger.error(f"Xatolik: {e}")
        await update.message.reply_text(f"Xatolik: {e}")


async def handle_feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle feedback button clicks."""
    global is_positive, response_text
    query = update.callback_query
    data = query.data
    user_id = update.effective_user.id

    if data == 'feedback_yes':
        response_text = "Rahmat! Sizning fikringiz qabul qilindi. 🙂"
        is_positive = True
    elif data == 'feedback_no':
        response_text = "Rahmat! Sizning fikringiz qabul qilindi. 🙂"
        is_positive = False

    # Store feedback in the database
    user_feedback = UserFeedbacks(user_id=user_id, is_positive=is_positive, text=last_message)
    user_feedback.add_feedback()

    await query.answer()
    await query.edit_message_text(text=response_text)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("tips", tips))
    application.add_handler(CommandHandler("check", check))
    application.add_handler(CommandHandler("report", report))

    # Add message handlers for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(MessageHandler(filters.CAPTION & ~filters.COMMAND, handle_caption))
    application.add_handler(CallbackQueryHandler(handle_save_preference, pattern='^save_'))
    application.add_handler(CallbackQueryHandler(handle_feedback, pattern='^feedback_'))

    print(application.chat_data)
    # Start polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
