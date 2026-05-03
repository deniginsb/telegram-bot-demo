#!/usr/bin/env python3
"""
Demo Telegram Bot - Portfolio untuk Freelance
Fitur: Auto-reply, Referral system, Inline keyboard, Database
"""

import json
import os
from datetime import datetime

# ===== DATABASE (JSON file-based) =====
DB_FILE = "bot_database.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}, "referrals": {}, "stats": {"total_users": 0, "total_referrals": 0}}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# ===== BOT LOGIC (python-telegram-bot) =====
"""
Install: pip install python-telegram-bot

Bot ini bisa di-deploy di:
- VPS/Raspberry Pi (24/7)
- Railway.app (gratis)
- Render.com (gratis)
- Koyeb (gratis)
"""

# --- Contoh struktur bot ---

BOT_TOKEN = "YOUR_BOT_TOKEN"  # Dapet dari @BotFather

# Commands yang tersedia:
COMMANDS = {
    "/start": "Mulai bot & dapat link referral",
    "/help": "Bantuan & daftar command",
    "/stats": "Lihat statistik",
    "/referral": "Lihat link referral kamu",
}

# Auto-reply rules
AUTO_REPLIES = {
    "halo": "Halo! Selamat datang 👋",
    "harga": "Silakan cek harga di /help",
    "terima kasih": "Sama-sama! 😊",
}

# ===== REFERRAL SYSTEM =====
"""
Setiap user dapat unique referral link:
https://t.me/BotUsername?start=REF_user123

Ketika user baru klik link itu:
1. User baru terdaftar
2. User yang ngasih link dapat point
3. Bisa dipake buat leaderboard / reward
"""

def generate_referral_code(user_id):
    return f"REF_{user_id}"

def track_referral(new_user_id, referrer_code):
    db = load_db()
    
    # Cari siapa yang punya referral code ini
    referrer_id = None
    for uid, user_data in db["users"].items():
        if user_data.get("referral_code") == referrer_code:
            referrer_id = uid
            break
    
    if referrer_id and referrer_id != str(new_user_id):
        # Update referrer's count
        db["users"][referrer_id]["referrals_count"] = db["users"][referrer_id].get("referrals_count", 0) + 1
        db["stats"]["total_referrals"] += 1
        
        # Track siapa yang di-refer
        if referrer_id not in db["referrals"]:
            db["referrals"][referrer_id] = []
        db["referrals"][referrer_id].append(str(new_user_id))
        
        save_db(db)
        return True
    return False

def register_user(user_id, username, first_name, referrer_code=None):
    db = load_db()
    
    if str(user_id) not in db["users"]:
        db["users"][str(user_id)] = {
            "username": username,
            "first_name": first_name,
            "referral_code": generate_referral_code(user_id),
            "referrals_count": 0,
            "joined_at": datetime.now().isoformat(),
            "is_active": True
        }
        db["stats"]["total_users"] += 1
        save_db(db)
        
        # Track referral jika ada
        if referrer_code:
            track_referral(user_id, referrer_code)
        
        return True
    return False

# ===== CONTOH HANDLER =====

"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

async def start(update: Update, context):
    user = update.effective_user
    args = context.args
    
    referrer_code = args[0] if args else None
    is_new = register_user(user.id, user.username, user.first_name, referrer_code)
    
    referral_link = f"https://t.me/BOT_USERNAME?start={generate_referral_code(user.id)}"
    
    keyboard = [
        [InlineKeyboardButton("📊 Statistik", callback_data="stats"),
         InlineKeyboardButton("🔗 Referral Saya", callback_data="referral")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = f"""
🤖 Selamat datang, {user.first_name}!

Gunakan bot ini untuk:
• Fitur 1
• Fitur 2  
• Fitur 3

🔗 Link referral kamu:
{referral_link}

Bagikan link ini dan dapatkan point!
    """
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def help_command(update: Update, context):
    help_text = "📋 Daftar Command:\n\n"
    for cmd, desc in COMMANDS.items():
        help_text += f"{cmd} - {desc}\n"
    await update.message.reply_text(help_text)

async def stats(update: Update, context):
    db = load_db()
    stats = db["stats"]
    user_stats = db["users"].get(str(update.effective_user.id), {})
    
    text = f"""
📊 Statistik Bot:
━━━━━━━━━━━━━━━
👥 Total Users: {stats['total_users']}
🔗 Total Referrals: {stats['total_referrals']}

📊 Statistik Kamu:
━━━━━━━━━━━━━━━
👤 Referral Code: {user_stats.get('referral_code', 'N/A')}
🎪 Referral Count: {user_stats.get('referrals_count', 0)}
📅 Bergabung: {user_stats.get('joined_at', 'N/A')[:10]}
    """
    await update.message.reply_text(text)

async def handle_message(update: Update, context):
    text = update.message.text.lower()
    
    for trigger, reply in AUTO_REPLIES.items():
        if trigger in text:
            await update.message.reply_text(reply)
            return

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()
"""

# ===== OUTPUT: File-file yang perlu di-upload ke GitHub =====
print("""
=== DEMO BOT TELEGRAM - PORTFOLIO ===

File yang perlu dibuat:
1. bot.py - Main bot code
2. database.py - Database handling
3. requirements.txt - Dependencies
4. README.md - Documentation
5. .env - Environment variables (jangan di-upload)

Tech Stack:
- Python 3.10+
- python-telegram-bot library
- JSON database (gampang upgrade ke SQLite/PostgreSQL)

Features untuk demo:
✅ Auto-reply system
✅ Referral system dengan tracking
✅ Inline keyboard buttons
✅ User database
✅ Statistics command
✅ Help command
✅ Clean code structure

Deploy options (GRATIS):
- Railway.app (recommended)
- Render.com
- Koyeb.com
- VPS sendiri

Nilai jual: 500rb - 2jt tergantung fitur
""")
