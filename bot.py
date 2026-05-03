#!/usr/bin/env python3
"""
Bot Telegram - Portfolio Demo
Fitur: Auto-reply, Referral system, Inline keyboard, Database
"""

import json
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# ===== CONFIG =====
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
DB_FILE = "bot_database.json"

# ===== DATABASE =====
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}, "referrals": {}, "stats": {"total_users": 0, "total_referrals": 0}}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ===== REFERRAL SYSTEM =====
def generate_referral_code(user_id):
    return f"REF_{user_id}"

def register_user(user_id, username, first_name, referrer_code=None):
    db = load_db()
    if str(user_id) not in db["users"]:
        db["users"][str(user_id)] = {
            "username": username,
            "first_name": first_name,
            "referral_code": generate_referral_code(user_id),
            "referrals_count": 0,
            "joined_at": datetime.now().isoformat(),
        }
        db["stats"]["total_users"] += 1
        save_db(db)

        if referrer_code:
            for uid, udata in db["users"].items():
                if udata.get("referral_code") == referrer_code and uid != str(user_id):
                    db["users"][uid]["referrals_count"] = db["users"][uid].get("referrals_count", 0) + 1
                    db["stats"]["total_referrals"] += 1
                    save_db(db)
                    break
        return True
    return False

# ===== AUTO-REPLIES =====
AUTO_REPLIES = {
    "halo": "Halo! Selamat datang 👋 Ketik /start untuk memulai.",
    "harga": "Silakan ketik /help untuk info lengkap.",
    "terima kasih": "Sama-sama! 😊",
}

# ===== COMMANDS =====
async def start(update: Update, context):
    user = update.effective_user
    args = context.args
    referrer_code = args[0] if args else None
    register_user(user.id, user.username, user.first_name, referrer_code)

    referral_link = f"https://t.me/BOT_USERNAME?start={generate_referral_code(user.id)}"

    keyboard = [
        [InlineKeyboardButton("📊 Statistik", callback_data="stats"),
         InlineKeyboardButton("🔗 Referral Saya", callback_data="referral")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🤖 Halo, {user.first_name}!\n\n"
        f"Selamat datang di bot demo ini.\n\n"
        f"🔗 Link referral kamu:\n{referral_link}\n\n"
        f"Bagikan link ini ke teman!",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context):
    text = (
        "📋 Daftar Command:\n\n"
        "/start - Mulai bot & dapat link referral\n"
        "/help - Bantuan & daftar command\n"
        "/stats - Lihat statistik bot\n"
        "/referral - Lihat link referral kamu\n"
    )
    await update.message.reply_text(text)

async def stats(update: Update, context):
    db = load_db()
    s = db["stats"]
    await update.message.reply_text(
        f"📊 Statistik Bot:\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👥 Total Users: {s['total_users']}\n"
        f"🔗 Total Referrals: {s['total_referrals']}"
    )

async def referral(update: Update, context):
    user = update.effective_user
    db = load_db()
    udata = db["users"].get(str(user.id), {})
    link = f"https://t.me/BOT_USERNAME?start={udata.get('referral_code', 'N/A')}"
    count = udata.get("referrals_count", 0)
    await update.message.reply_text(
        f"🔗 Referral Info:\n"
        f"━━━━━━━━━━━━━━━\n"
        f"Link: {link}\n"
        f"Jumlah referral: {count}"
    )

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "stats":
        db = load_db()
        s = db["stats"]
        await query.edit_message_text(
            f"📊 Statistik Bot:\n"
            f"👥 Total Users: {s['total_users']}\n"
            f"🔗 Total Referrals: {s['total_referrals']}"
        )
    elif query.data == "referral":
        user = query.from_user
        db = load_db()
        udata = db["users"].get(str(user.id), {})
        link = f"https://t.me/BOT_USERNAME?start={udata.get('referral_code', 'N/A')}"
        await query.edit_message_text(f"🔗 Link referral kamu:\n{link}")
    elif query.data == "help":
        await query.edit_message_text(
            "📋 Command:\n/start - Mulai\n/help - Bantuan\n/stats - Statistik\n/referral - Referral"
        )

async def handle_message(update: Update, context):
    text = update.message.text.lower()
    for trigger, reply in AUTO_REPLIES.items():
        if trigger in text:
            await update.message.reply_text(reply)
            return

# ===== MAIN =====
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("referral", referral))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
