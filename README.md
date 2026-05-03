# Bot Telegram - Portfolio Demo

Bot Telegram dengan fitur lengkap untuk kebutuhan bisnis dan komunitas.

## Fitur

- ✅ **Auto-Reply System** - Balas otomatis berdasarkan keyword
- ✅ **Referral System** - Track user & referral link
- ✅ **Inline Keyboard** - Tombol interaktif
- ✅ **User Database** - Simpan data user
- ✅ **Statistics** - Statistik penggunaan bot
- ✅ **Help Command** - Panduan penggunaan

## Tech Stack

- Python 3.10+
- python-telegram-bot
- JSON Database (bisa upgrade ke SQLite/PostgreSQL)

## Cara Install

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/telegram-bot-demo.git
cd telegram-bot-demo

# Install dependencies
pip install -r requirements.txt

# Set bot token
export BOT_TOKEN="your_bot_token_from_botfather"

# Jalankan bot
python bot.py
```

## Deploy (Gratis)

### Railway.app
1. Push ke GitHub
2. Buka railway.app
3. New Project > Deploy from GitHub
4. Add environment variable: `BOT_TOKEN`
5. Deploy!

### Render.com
1. Push ke GitHub
2. Buka render.com
3. New > Web Service
4. Connect GitHub repo
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `python bot.py`
7. Add environment variable: `BOT_TOKEN`

## Demo

Bot ini bisa dikustomisasi untuk:
- Bot komunitas (moderasi, welcome, role)
- Bot bisnis (auto-reply, order system)
- Bot crypto (price alert, portfolio tracker)
- Bot referral (tracking, leaderboard)

## Contact

Butuh bot custom? Hubungi saya untuk konsultasi gratis.

---

*Built with ❤️ by Deni*
