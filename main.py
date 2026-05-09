import os
import yt_dlp
import requests
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = "TOKENINGIZNI_YOZING"
CHANNEL_USERNAME = "@VibeSavechannel"

DOWNLOAD_PATH = "downloads"

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)


# ================= MAJBURIY OBUNA =================

async def check_sub(user_id, bot):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    subscribed = await check_sub(user.id, context.bot)

    if not subscribed:
        keyboard = [
            [
                InlineKeyboardButton(
                    "📢 Kanalga qo‘shilish",
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                )
            ],
            [
                InlineKeyboardButton(
                    "✅ Tekshirish",
                    callback_data="check_sub"
                )
            ]
        ]

        await update.message.reply_text(
            "❌ Botdan foydalanish uchun kanalga obuna bo‘ling.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    text = """
🔥 Video yuklovchi bot

✅ Platformalar:
• Instagram
• TikTok
• YouTube
• Facebook
• Pinterest
• Snapchat
• Threads
• Likee

📥 Link yuboring yoki YouTube qidiruv yozing.
"""

    await update.message.reply_text(text)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    subscribed = await check_sub(query.from_user.id, context.bot)

    if subscribed:
        await query.message.edit_text(
            "✅ Obuna tasdiqlandi.\n\nEndi link yuboring."
        )
    else:
        await query.answer(
            "❌ Hali kanalga qo‘shilmagansiz.",
            show_alert=True
        )


# ================= VIDEO YUKLASH =================

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    subscribed = await check_sub(user.id, context.bot)

    if not subscribed:
        keyboard = [
            [
                InlineKeyboardButton(
                    "📢 Kanalga qo‘shilish",
                    url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                )
            ]
        ]

        await update.message.reply_text(
            "❌ Avval kanalga obuna bo‘ling.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    text = update.message.text

    msg = await update.message.reply_text("⏳ Yuklanmoqda...")

    try:

        # ============ YOUTUBE SEARCH ============
        if "http" not in text:

            ydl_opts = {
                "format": "best",
                "quiet": True,
                "noplaylist": True,
                "default_search": "ytsearch1",
                "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",
                "nocheckcertificate": True,
                "ignoreerrors": True,
                "geo_bypass": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)

                if "entries" in info:
                    info = info["entries"][0]

                file_path = ydl.prepare_filename(info)

        # ============ LINK DOWNLOAD ============
        else:

            ydl_opts = {
                "format": "best",
                "outtmpl": f"{DOWNLOAD_PATH}/%(title)s.%(ext)s",

                "quiet": True,
                "nocheckcertificate": True,
                "ignoreerrors": True,
                "no_warnings": True,

                "geo_bypass": True,
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(text, download=True)
                file_path = ydl.prepare_filename(info)

        # ============ VIDEO YUBORISH ============

        caption = f"""
✅ Yuklandi

🎬 {info.get('title', 'Video')}
"""

        with open(file_path, "rb") as video:
            await update.message.reply_video(
                video=video,
                caption=caption
            )

        os.remove(file_path)

        await msg.delete()

    except Exception as e:
        await msg.edit_text(
            f"❌ Xato:\n{str(e)}"
        )


# ================= MAIN =================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(CallbackQueryHandler(button))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            download_video
        )
    )

    print("BOT ISHLADI ✅")

    app.run_polling()


if __name__ == "__main__":
    main()
