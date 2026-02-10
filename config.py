import os
from dotenv import load_dotenv

load_dotenv()

# Bot Token (from environment variables)
BOT_TOKEN = os.getenv("BOT_TOKEN", "8585417637:AAHI022IQTD28YKh43a3rb29vipcpEEGqGg")

# Channel and link configuration
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "https://t.me/rolex9au")
FREE_SPIN_URL = os.getenv("FREE_SPIN_URL", "https://rolex9au.com/RFROLEX9BOT")
FREE_CREDIT_URL = os.getenv("FREE_CREDIT_URL", "https://rolex9au.com/RFROLEX9BOT")

# Promotional images (local file paths - hardcoded in code)
FREE_SPIN_IMAGE_PATH = "public/free_spin.jpg"
HOT_GAME_TIPS_IMAGE_PATH = "public/hot_game_tips.jpg"

# Bot information
BOT_NAME = "Rolex9 Promo Bot"
BOT_DESCRIPTION = "Rolex9 Marketing Assistant - Provides latest promotions and event information"
