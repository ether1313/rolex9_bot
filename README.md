# Rolex9 Promo Bot 🎰

A full-featured Telegram marketing bot with custom keyboard, promotional messages, admin management, and bulk messaging capabilities.

## ✨ Features

- 🎯 **Main Menu** - Display main menu with custom keyboard when users send `/start`
- ⌨️ **Custom Keyboard** - Interactive buttons at the bottom for easy navigation
- 📢 **Promotional Messages** - Send promotional messages with images and text
- 🔘 **Interactive Buttons** - Inline buttons in messages that can jump to external links or channels
- 👑 **Admin Management** - Complete admin system with user management
- 📊 **User Statistics** - Track total users who started the bot
- 📤 **Bulk Messaging** - Send messages to all users via forwarding or `/mailing` command
- 💾 **Data Persistence** - User stats and admin data saved to JSON files

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHANNEL=https://t.me/your_channel
FREE_SPIN_URL=https://your_free_spin_link
FREE_CREDIT_URL=https://your_free_credit_link
DATA_DIR=/data
```

**Note:** If not set, the bot will use default values from `config.py`.

### 3. Get Bot Token

1. Search for `@BotFather` in Telegram
2. Send `/newbot` to create a new bot
3. Follow the prompts to set bot name and username
4. Copy the Bot Token to the `.env` file

### 4. Prepare Promotional Images (Optional)

Place promotional images in the `public/` directory:
- `public/free_spin.jpg` - Image for free spin promotion
- `public/hot_game_tips.jpg` - Image for hot game tips channel

If images are not provided, the bot will send text-only messages.

### 5. Run Bot Locally

```bash
python bot.py
```

## 📁 Project Structure

```
rolex9_bot/
├── bot.py              # Main bot file with all handlers
├── config.py           # Configuration file with environment variables
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration for deployment
├── fly.toml            # Fly.io deployment configuration
├── DEPLOY.md           # Deployment guide (Chinese)
├── README.md           # Project documentation
├── public/             # Promotional images directory
│   ├── free_spin.jpg
│   └── hot_game_tips.jpg
└── data/               # Data directory (created at runtime)
    ├── user_stats.json # User statistics
    └── admins.json     # Admin list
```

## 🎮 Usage

### Bot Commands

#### User Commands
- `/start` - Display main menu with custom keyboard

#### Admin Commands
- `/stats` - Show total number of users who started the bot
- `/setadmin <user_id>` - Add a user as administrator
- `/removeadmin <user_id>` - Remove a user from administrators
- `/listadmins` - List all administrators
- `/data` - View admins and user statistics (shows first 20 users)
- `/mailing` - Send the replied message to all users
- `/test_mailing` - Test mailing functionality (debug command)

### Button Functions

1. **GET FREE SPIN ON ROLEX9 🎰** - Shows free spin promotional information with inline buttons:
   - `CHEKC FREE SPIN ON WEB 🎁` - Links to free spin URL
   - `TELEGRAM CHANNEL ❤️` - Links to Telegram channel

2. **HOT GAME TIPS CHANNEL 🍒** - Shows hot game tips channel information with inline buttons:
   - `FREE CREDIT GIFT 🎁` - Links to free credit URL
   - `HOT CHANNEL 🤑` - Links to Telegram channel

### Admin Features

#### Setting Up First Admin
The first user to send `/setadmin` becomes the first administrator. After that, only existing admins can add new admins.

#### Bulk Messaging
Admins can send messages to all users in two ways:

1. **Forward Message** - Simply forward any message (photo, video, document, or text) to the bot, and it will automatically send to all users
2. **Reply with /mailing** - Reply to any message with `/mailing` command to send it to all users

The bot prioritizes forwarding messages to preserve Premium emoji and formatting. If forwarding fails, it falls back to resending the message.

## 🔧 Configuration

### Environment Variables

All configuration is done through environment variables or `.env` file:

- `BOT_TOKEN` (Required) - Telegram Bot Token from @BotFather
- `TELEGRAM_CHANNEL` (Optional) - Telegram channel URL (default: `https://t.me/rolex9`)
- `FREE_SPIN_URL` (Optional) - Free spin promotion URL (default: `https://rolex9.com/RFROLEX9BOT9`)
- `FREE_CREDIT_URL` (Optional) - Free credit promotion URL (default: `https://rolex9.com/RFROLEX9BOT9`)
- `DATA_DIR` (Optional) - Directory for data files (default: `/data` for Fly.io, current directory for local)

### Customization

#### Modify Promotional Text

Edit the text content in `bot.py`:

```python
# In handle_get_free_spin() function
promo_text = """Your promotional text..."""

# In handle_hot_game_tips() function
channel_text = """Your channel text..."""
```

#### Modify Image Paths

Edit `config.py` to change image paths:

```python
FREE_SPIN_IMAGE_PATH = "public/free_spin.jpg"
HOT_GAME_TIPS_IMAGE_PATH = "public/hot_game_tips.jpg"
```

## 🛠️ Deployment

### Local Development

```bash
python bot.py
```

### Docker Deployment

Build and run with Docker:

```bash
docker build -t rolex9-bot .
docker run -d --env-file .env rolex9-bot
```

### Fly.io Deployment

This bot is configured for deployment on Fly.io. See `DEPLOY.md` for detailed deployment instructions.

**Quick deployment steps:**

1. Install Fly CLI and login: `fly auth login`
2. Create volume: `fly volumes create rolex9_bot_data --size 1 --region sin`
3. Set secrets: `fly secrets set BOT_TOKEN="your_token"`
4. Deploy: `fly deploy`

The bot uses Fly.io volumes for data persistence, ensuring user stats and admin data survive container restarts.

## 📝 Notes

1. **Keep Bot Token secret** - Do not commit `.env` file or hardcode tokens in code
2. **Data Persistence** - On Fly.io, data is stored in `/data` volume. Locally, data is stored in the current directory
3. **Image Support** - Promotional images are optional. If not found, the bot sends text-only messages
4. **Admin System** - The first user to use `/setadmin` becomes the first admin. At least one admin must always exist
5. **Message Forwarding** - The bot prioritizes forwarding messages to preserve Premium emoji and formatting

## 🔍 Troubleshooting

### Bot not responding
- Check if `BOT_TOKEN` is set correctly
- Check logs for error messages
- Verify the bot is running and connected to Telegram

### Mailing not working
- Ensure you are an admin (use `/setadmin` first)
- Check if there are users in the database (use `/stats`)
- Verify the message has content (photo, video, document, or text)

### Data not persisting
- On Fly.io: Ensure volume is mounted correctly (check `fly.toml`)
- Locally: Check if `DATA_DIR` has write permissions

## 📞 Support

If you encounter issues, please check:
- Whether the Bot Token is correct
- Whether environment variables are set properly
- Whether the network connection is normal
- Error messages in log files
- Fly.io logs: `fly logs` (if deployed on Fly.io)

## 📄 License

MIT License

---

**Rolex9 Promo Bot** - Making marketing simpler! 🚀
