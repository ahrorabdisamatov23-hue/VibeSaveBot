from telebot import TeleBot, types
import yt_dlp
import os

TOKEN = "8684094849:AAGu4Q4CbeZ8iUYKYg56sc4zXSQSdQ66Odk"
CHANNEL = "@VibeSavechannel"

bot = TeleBot(TOKEN, parse_mode="HTML")

search_results = {}


# START
@bot.message_handler(commands=['start'])
def start(message):

    text = """
<b>🔥 ASSALOMU ALAYKUM!</b>

<b>Bot orqali quyidagilarni yuklab olishingiz mumkin:</b>

• INSTAGRAM
• TIKTOK
• YOUTUBE
• FACEBOOK
• PINTEREST
• SNAPCHAT
• THREADS
• LIKEE

<b>🎵 QO‘SHIQ QIDIRISH MAVJUD</b>

<b>🚀 Link yoki musiqa nomini yuboring</b>

<b>😎 BOT GURUHLARDA HAM ISHLAYDI!</b>
"""

    markup = types.InlineKeyboardMarkup()

    group_btn = types.InlineKeyboardButton(
        "👥 Guruhga qo‘shish",
        url="https://t.me/VibeSave24Bot?startgroup=true"
    )

    markup.add(group_btn)

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )


# OBUNA
def subscribed(user_id):

    try:

        member = bot.get_chat_member(CHANNEL, user_id)

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:
        return False


# TEKSHIRISH
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):

    if subscribed(call.from_user.id):

        bot.answer_callback_query(
            call.id,
            "✅ Tasdiqlandi!"
        )

        bot.send_message(
            call.message.chat.id,
            "<b>✅ Endi musiqa yoki video qidiring 🎵</b>"
        )

    else:

        bot.answer_callback_query(
            call.id,
            "❌ Hali obuna bo‘lmagansiz!",
            show_alert=True
        )


# MUSIQA TANLASH
@bot.callback_query_handler(func=lambda call: call.data.startswith("music_"))
def download_music(call):

    index = int(call.data.split("_")[1])

    data = search_results.get(call.message.chat.id)

    if not data:
        return

    song = data[index]

    wait = bot.send_message(
        call.message.chat.id,
        "<b>⏳ Yuklanmoqda...</b>"
    )

    try:

        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(
                song["url"],
                download=True
            )

            filename = ydl.prepare_filename(info)

            title = info.get("title", "Music")

            thumbnail = info.get("thumbnail")

        buttons = types.InlineKeyboardMarkup(row_width=2)

        share_btn = types.InlineKeyboardButton(
            "📤 Ulashish",
            switch_inline_query=title
        )

        group_btn = types.InlineKeyboardButton(
            "👥 Guruhga qo‘shish",
            url="https://t.me/VibeSave24Bot?startgroup=true"
        )

        buttons.add(share_btn, group_btn)

        caption = f"""
🎵 <b>{title}</b>

🚀 <a href="https://t.me/VibeSave24Bot">@VibeSave24Bot</a> orqali yuklab olindi
"""

        with open(filename, "rb") as audio:

            bot.send_audio(
                call.message.chat.id,
                audio,
                caption=caption,
                thumb=thumbnail,
                reply_markup=buttons
            )

        os.remove(filename)

        bot.delete_message(
            call.message.chat.id,
            wait.message_id
        )

    except Exception as e:

        bot.edit_message_text(
            f"<b>❌ Xatolik:</b>\n<code>{e}</code>",
            call.message.chat.id,
            wait.message_id
        )


# ASOSIY HANDLER
@bot.message_handler(func=lambda message: True)
def downloader(message):

    if message.text.startswith("/"):
        return

    # OBUNA TEKSHIRISH
    if not subscribed(message.from_user.id):

        markup = types.InlineKeyboardMarkup()

        sub_btn = types.InlineKeyboardButton(
            "📢 Kanalga obuna bo‘lish",
            url=f"https://t.me/{CHANNEL.replace('@','')}"
        )

        check_btn = types.InlineKeyboardButton(
            "✅ Tekshirish",
            callback_data="check_sub"
        )

        markup.add(sub_btn)
        markup.add(check_btn)

        bot.send_message(
            message.chat.id,
            """
<b>❌ Botdan to‘liq foydalanish uchun quyidagi kanalga obuna bo‘ling!</b>
""",
            reply_markup=markup
        )

        return

    text = message.text

    # LINK BO‘LSA VIDEO
    if text.startswith(("http://", "https://")):

        wait = bot.send_message(
            message.chat.id,
            "<b>⏳ Video yuklanmoqda...</b>"
        )

        try:

            ydl_opts = {
                'format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                info = ydl.extract_info(
                    text,
                    download=True
                )

                filename = ydl.prepare_filename(info)

                title = info.get("title", "Video")

            buttons = types.InlineKeyboardMarkup(row_width=2)

            share_btn = types.InlineKeyboardButton(
                "📤 Ulashish",
                switch_inline_query=title
            )

            group_btn = types.InlineKeyboardButton(
                "👥 Guruhga qo‘shish",
                url="https://t.me/VibeSave24Bot?startgroup=true"
            )

            buttons.add(share_btn, group_btn)

            caption = """
🚀 <a href="https://t.me/VibeSave24Bot">@VibeSave24Bot</a> orqali yuklab olindi
"""

            with open(filename, "rb") as video:

                bot.send_video(
                    message.chat.id,
                    video,
                    caption=caption,
                    reply_markup=buttons
                )

            os.remove(filename)

            bot.delete_message(
                message.chat.id,
                wait.message_id
            )

        except Exception as e:

            bot.edit_message_text(
                f"<b>❌ Xatolik:</b>\n<code>{e}</code>",
                message.chat.id,
                wait.message_id
            )

    # MUSIQA SEARCH
    else:

        try:

            with yt_dlp.YoutubeDL({}) as ydl:

                info = ydl.extract_info(
                    f"ytsearch5:{text}",
                    download=False
                )

            results = info["entries"]

            search_results[message.chat.id] = results

            result_text = "🎵 <b>Qidiruv natijalari:</b>\n\n"

            markup = types.InlineKeyboardMarkup(row_width=5)

            buttons = []

            for i, item in enumerate(results):

                title = item["title"]

                result_text += f"{i+1}. {title[:45]}\n"

                btn = types.InlineKeyboardButton(
                    f"{i+1}",
                    callback_data=f"music_{i}"
                )

                buttons.append(btn)

            markup.add(*buttons)

            bot.send_message(
                message.chat.id,
                result_text,
                reply_markup=markup
            )

        except Exception as e:

            bot.send_message(
                message.chat.id,
                f"<b>❌ Xatolik:</b>\n<code>{e}</code>"
            )


# GURUH
@bot.my_chat_member_handler()
def added(message):

    status = message.new_chat_member.status

    if status in ["member", "administrator"]:

        bot.send_message(
            message.chat.id,
            """
<b>🔥 VibeSaveBot guruhga qo‘shildi!</b>

<b>🚀 Endi link yuborsangiz yuklab beradi.</b>
"""
        )


print("BOT ISHLADI...")
bot.infinity_polling()
