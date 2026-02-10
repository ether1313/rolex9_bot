from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import json
import os
from config import BOT_TOKEN, TELEGRAM_CHANNEL, FREE_SPIN_URL, FREE_CREDIT_URL, FREE_SPIN_IMAGE_PATH, HOT_GAME_TIPS_IMAGE_PATH

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# File to store user statistics
# Use volume path for persistence on Fly.io, fallback to current directory for local development
DATA_DIR = os.getenv("DATA_DIR", "/data")
# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

STATS_FILE = os.path.join(DATA_DIR, "user_stats.json")
ADMINS_FILE = os.path.join(DATA_DIR, "admins.json")  # File to store admin list


def load_user_stats():
    """Load user statistics from file"""
    if os.path.exists(STATS_FILE):
        try:
            with open(STATS_FILE, 'r') as f:
                data = json.load(f)
                # Ensure users is a list
                if "users" in data and isinstance(data["users"], list):
                    return data
                return {"users": []}
        except (json.JSONDecodeError, IOError):
            return {"users": []}
    return {"users": []}


def save_user_stats(stats):
    """Save user statistics to file"""
    # Convert set to list for JSON serialization
    stats_to_save = {"users": list(stats["users"])}
    with open(STATS_FILE, 'w') as f:
        json.dump(stats_to_save, f)


def add_user(user_id):
    """Add user to statistics"""
    stats = load_user_stats()
    # Use set to avoid duplicates, then convert back to list
    users_set = set(stats["users"])
    users_set.add(user_id)
    stats["users"] = list(users_set)
    save_user_stats(stats)


def get_total_users():
    """Get total number of users"""
    stats = load_user_stats()
    # Remove duplicates using set, then return count
    return len(set(stats["users"]))


# Admin management functions
def load_admins():
    """Load admin list from file"""
    if os.path.exists(ADMINS_FILE):
        try:
            with open(ADMINS_FILE, 'r') as f:
                data = json.load(f)
                if "admins" in data and isinstance(data["admins"], list):
                    return data
                return {"admins": []}
        except (json.JSONDecodeError, IOError):
            return {"admins": []}
    return {"admins": []}


def save_admins(admins_data):
    """Save admin list to file"""
    with open(ADMINS_FILE, 'w') as f:
        json.dump(admins_data, f)


def is_admin(user_id):
    """Check if user is an admin"""
    admins_data = load_admins()
    return user_id in admins_data.get("admins", [])


def add_admin(user_id):
    """Add user to admin list"""
    admins_data = load_admins()
    admins_set = set(admins_data.get("admins", []))
    admins_set.add(user_id)
    admins_data["admins"] = list(admins_set)
    save_admins(admins_data)


def remove_admin(user_id):
    """Remove user from admin list"""
    admins_data = load_admins()
    admins_list = admins_data.get("admins", [])
    if user_id in admins_list:
        admins_list.remove(user_id)
        admins_data["admins"] = admins_list
        save_admins(admins_data)
        return True
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - show main menu"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    # Add user to statistics
    add_user(user.id)
    
    # Create custom keyboard (bottom buttons) - only menu options
    keyboard = [
        [
            KeyboardButton(text="GET FREE SPIN ON ROLEX9 🎰"),
            KeyboardButton(text="HOT GAME TIPS CHANNEL 🍒")
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    # Send keyboard buttons only
    await update.message.reply_text(
        "Main Menu",
        reply_markup=reply_markup
    )


async def handle_get_free_spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GET FREE SPIN button click"""
    promo_text = """🎖 ROLEX9 Welcomes You to The Pinnacle of Online Gaming.

🎁 Sign up today and instantly claim your complimentary A$199.99 bonus — no deposit required.
🎡 Return daily to spin our exclusive Prize Wheel and secure rewards of up to A$999.
🚀 Amplify your winnings with a 100% first-deposit match, doubling your funds for maximum impact from day one.
👑 Step into our VIP realm — enjoy meticulously tailored perks, unlock weekly rewards up to A$1,099, and experience seamless, transparent bonuses combined with premium, high-stakes gameplay.

💎 At ROLEX9, we deliver elite-level entertainment for Australian players. Play boldly. Win exceptionally. 🎰✨"""
    
    # Create inline buttons (vertical layout - each button on its own row)
    inline_keyboard = [
        [InlineKeyboardButton("CHEKC FREE SPIN ON WEB 🎁", url=FREE_SPIN_URL)],
        [InlineKeyboardButton("TELEGRAM CHANNEL ❤️", url=TELEGRAM_CHANNEL)]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    
    # Send image if file exists, otherwise send text only
    if os.path.exists(FREE_SPIN_IMAGE_PATH):
        with open(FREE_SPIN_IMAGE_PATH, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=promo_text,
                reply_markup=inline_markup
            )
    else:
        await update.message.reply_text(promo_text, reply_markup=inline_markup)


async def handle_hot_game_tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle HOT GAME TIPS CHANNEL button click"""
    channel_text = """ROLEX9: Big Rewards. No Nonsense. 🎉

🔥 Welcome Bonus A$99 FREE — No deposit required.
🎰 Spin the Wheel Daily: Win up to A$199.
💎 Random Second Withdraw — exclusive to ROLEX9.
👑 VIP experience: daily perks + weekly rewards up to A$8,888.

✨ Elite games. Transparent bonuses. Instant payouts.
🚀 ROLEX9 — Your Instant WIN Destination!"""
    
    # Create inline buttons (vertical layout - each button on its own row)
    inline_keyboard = [
        [InlineKeyboardButton("FREE CREDIT GIFT 🎁", url=FREE_CREDIT_URL)],
        [InlineKeyboardButton("HOT CHANNEL 🤑", url=TELEGRAM_CHANNEL)]
    ]
    inline_markup = InlineKeyboardMarkup(inline_keyboard)
    
    # Send image if file exists, otherwise send text only
    if os.path.exists(HOT_GAME_TIPS_IMAGE_PATH):
        with open(HOT_GAME_TIPS_IMAGE_PATH, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=channel_text,
                reply_markup=inline_markup
            )
    else:
        await update.message.reply_text(channel_text, reply_markup=inline_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages"""
    message = update.message
    user_id = update.effective_user.id
    text = message.text
    
    # Check if admin is trying to mailing (by replying to a message or sending media)
    # Allow admins to mailing by sending messages directly (not just forwarding)
    if is_admin(user_id) and (message.photo or message.video or message.document or (text and len(text) > 10)):
        # Check if this looks like a mailing message (has media or long text)
        # But only if it's not a command or button text
        if text and ("GET FREE SPIN" not in text.upper() and "HOT GAME TIPS" not in text.upper()):
            # Admin is sending a message that might be for mailing
            # Ask for confirmation or auto-mailing
            # For now, we'll let the forwarded message handler take care of it
            # But we can add a /mailing command later if needed
            pass
    
    if "GET FREE SPIN" in text.upper():
        await handle_get_free_spin(update, context)
    elif "HOT GAME TIPS" in text.upper():
        await handle_hot_game_tips(update, context)
    else:
        # Default reply
        await update.message.reply_text(
            "Please use the bottom buttons to interact, or send /start to view the main menu."
        )


async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stat command - show user statistics"""
    total_users = get_total_users()
    stat_message = f"📊 **Statistics**\n\nTotal users started: {total_users}"
    await update.message.reply_text(stat_message, parse_mode='Markdown')


async def setadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setadmin command - add admin (only existing admins can add new admins)"""
    user_id = update.effective_user.id
    
    # Check if user is already an admin
    if not is_admin(user_id):
        # If no admins exist, make this user the first admin
        admins_data = load_admins()
        if not admins_data.get("admins", []):
            add_admin(user_id)
            await update.message.reply_text(
                f"✅ You have been set as the first administrator!\n"
                f"Your User ID: {user_id}"
            )
            logger.info(f"User {user_id} became the first admin")
            return
        else:
            await update.message.reply_text(
                "❌ Access denied. Only administrators can add new admins."
            )
            return
    
    # Check if user ID is provided
    if not context.args:
        await update.message.reply_text(
            "Usage: /setadmin <user_id>\n\n"
            "Example: /setadmin 123456789\n\n"
            "To get a user's ID, ask them to message @userinfobot"
        )
        return
    
    try:
        new_admin_id = int(context.args[0])
        add_admin(new_admin_id)
        await update.message.reply_text(
            f"✅ User {new_admin_id} has been added as an administrator."
        )
        logger.info(f"Admin {user_id} added new admin {new_admin_id}")
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid user ID. Please provide a valid number."
        )


async def removeadmin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /removeadmin command - remove admin"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text(
            "❌ Access denied. Only administrators can remove admins."
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "Usage: /removeadmin <user_id>\n\n"
            "Example: /removeadmin 123456789"
        )
        return
    
    try:
        admin_to_remove = int(context.args[0])
        
        # Prevent removing yourself if you're the only admin
        admins_data = load_admins()
        if len(admins_data.get("admins", [])) <= 1:
            await update.message.reply_text(
                "❌ Cannot remove the last administrator."
            )
            return
        
        if remove_admin(admin_to_remove):
            await update.message.reply_text(
                f"✅ User {admin_to_remove} has been removed from administrators."
            )
            logger.info(f"Admin {user_id} removed admin {admin_to_remove}")
        else:
            await update.message.reply_text(
                f"❌ User {admin_to_remove} is not an administrator."
            )
    except ValueError:
        await update.message.reply_text(
            "❌ Invalid user ID. Please provide a valid number."
        )


async def listadmins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /listadmins command - list all admins"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text(
            "❌ Access denied. Only administrators can view the admin list."
        )
        return
    
    admins_data = load_admins()
    admins_list = admins_data.get("admins", [])
    
    if not admins_list:
        await update.message.reply_text("📋 No administrators found.")
        return
    
    admin_list_text = "📋 **Administrators:**\n\n"
    for admin_id in admins_list:
        admin_list_text += f"• `{admin_id}`\n"
    
    await update.message.reply_text(admin_list_text, parse_mode='Markdown')


async def view_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /data command - view admins and user stats data (admin only)"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text(
            "❌ Access denied. Only administrators can view data."
        )
        return
    
    # Load admins data
    admins_data = load_admins()
    admins_list = admins_data.get("admins", [])
    
    # Load user stats data
    stats = load_user_stats()
    user_ids = list(set(stats.get("users", [])))
    
    # Format admins data
    admins_text = "👑 **Admins:**\n"
    if admins_list:
        for admin_id in admins_list:
            admins_text += f"• `{admin_id}`\n"
    else:
        admins_text += "• No admins found\n"
    
    # Format users data
    users_text = f"\n👥 **Users (Total: {len(user_ids)}):**\n"
    if user_ids:
        # Show first 20 users, then count
        display_users = user_ids[:20]
        for user_id in display_users:
            users_text += f"• `{user_id}`\n"
        if len(user_ids) > 20:
            users_text += f"\n... and {len(user_ids) - 20} more users\n"
    else:
        users_text += "• No users found\n"
    
    # Combine and send
    data_text = admins_text + users_text
    
    # Telegram message limit is 4096 characters
    if len(data_text) > 4000:
        # Send in parts if too long
        part1 = admins_text + f"\n👥 **Users (Total: {len(user_ids)}):**\n"
        await update.message.reply_text(part1, parse_mode='Markdown')
        
        if user_ids:
            users_list = "\n".join([f"• `{uid}`" for uid in user_ids[:50]])
            if len(user_ids) > 50:
                users_list += f"\n... and {len(user_ids) - 50} more"
            await update.message.reply_text(users_list, parse_mode='Markdown')
    else:
        await update.message.reply_text(data_text, parse_mode='Markdown')


async def mailing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mailing command - mailing the replied message to all users"""
    user_id = update.effective_user.id
    message = update.message
    
    # Check admin permission
    if not is_admin(user_id):
        await update.message.reply_text(
            "❌ Access denied. Only administrators can mailing messages."
        )
        return
    
    # Check if message is a reply
    if not message.reply_to_message:
        await update.message.reply_text(
            "📤 **How to use /mailing:**\n\n"
            "1. Send or forward the post you want to mailing\n"
            "2. Reply to that message with /mailing\n\n"
            "Or simply forward a post to this bot (it will auto-detect and mailing)."
        )
        return
    
    # Get the replied message
    replied_message = message.reply_to_message
    
    # Load all users
    stats = load_user_stats()
    user_ids = list(set(stats["users"]))
    
    # Exclude admin from mailing list (admin already sees the message)
    user_ids = [uid for uid in user_ids if uid != user_id]
    
    if not user_ids:
        await update.message.reply_text("❌ No users found to mailing to (excluding yourself).")
        return
    
    # Confirm mailing start
    await update.message.reply_text(
        f"📤 Mailing to {len(user_ids)} users...\n"
        f"Please wait..."
    )
    
    success_count = 0
    failed_count = 0
    
    # Extract message content
    has_photo = replied_message.photo is not None and len(replied_message.photo) > 0
    has_video = replied_message.video is not None
    has_document = replied_message.document is not None
    caption = replied_message.caption
    text = replied_message.text if not (has_photo or has_video or has_document) else None
    
    logger.info(f"Mailing command - Photo: {has_photo}, Video: {has_video}, Document: {has_document}, Text: {text is not None}, Caption: {caption is not None}")
    
    # Check if we have any content to mailing
    if not (has_photo or has_video or has_document or text):
        await update.message.reply_text(
            "❌ Cannot mailing: Replied message has no content (photo, video, document, or text)."
        )
        return
    
    # Mailing to all users
    # Priority: Use forward_message to preserve Premium emoji and all formatting
    for target_user_id in user_ids:
        try:
            message_sent = False
            
            # First, try to forward the message (preserves Premium emoji and all formatting)
            try:
                await context.bot.forward_message(
                    chat_id=target_user_id,
                    from_chat_id=replied_message.chat_id,
                    message_id=replied_message.message_id
                )
                success_count += 1
                message_sent = True
                logger.info(f"Forwarded message to user {target_user_id} (preserving Premium emoji)")
            except Exception as forward_error:
                # If forwarding fails, fall back to resending (loses Premium emoji but ensures delivery)
                logger.warning(f"Forward failed for user {target_user_id}, trying to resend: {forward_error}")
                
                if has_photo:
                    photo = replied_message.photo[-1] if replied_message.photo else None
                    if photo and photo.file_id:
                        await context.bot.send_photo(
                            chat_id=target_user_id,
                            photo=photo.file_id,
                            caption=caption,
                            parse_mode='HTML' if caption else None
                        )
                        success_count += 1
                        message_sent = True
                        logger.info(f"Sent photo to user {target_user_id} (fallback)")
                elif has_video:
                    video = replied_message.video
                    if video and video.file_id:
                        await context.bot.send_video(
                            chat_id=target_user_id,
                            video=video.file_id,
                            caption=caption,
                            parse_mode='HTML' if caption else None
                        )
                        success_count += 1
                        message_sent = True
                        logger.info(f"Sent video to user {target_user_id} (fallback)")
                elif has_document:
                    document = replied_message.document
                    if document and document.file_id:
                        await context.bot.send_document(
                            chat_id=target_user_id,
                            document=document.file_id,
                            caption=caption,
                            parse_mode='HTML' if caption else None
                        )
                        success_count += 1
                        message_sent = True
                        logger.info(f"Sent document to user {target_user_id} (fallback)")
                elif text:
                    await context.bot.send_message(
                        chat_id=target_user_id,
                        text=text,
                        parse_mode='HTML'
                    )
                    success_count += 1
                    message_sent = True
                    logger.info(f"Sent text to user {target_user_id} (fallback)")
            
            if not message_sent:
                failed_count += 1
                logger.error(f"Failed to mailing to user {target_user_id}: All methods failed")
                    
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to mailing to user {target_user_id}: {e}", exc_info=True)
    
    # Report results
    result_message = (
        f"📥 Mailing completed!\n\n"
        f"✅️ Success: {success_count}\n"
        f"❌ Failed: {failed_count}\n"
        f"📝 Total: {len(user_ids)}"
    )
    await update.message.reply_text(result_message)


async def test_mailing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /test_mailing command - test if admin can mailing (for debugging)"""
    user_id = update.effective_user.id
    message = update.message
    
    # Check admin permission
    is_admin_user = is_admin(user_id)
    
    # Check if message is forwarded
    is_forwarded = bool(message.forward_from or message.forward_from_chat)
    
    # Get message info
    has_photo = message.photo is not None
    has_text = message.text is not None
    has_caption = message.caption is not None
    
    debug_info = (
        f"🔍 **Debug Info:**\n\n"
        f"Your User ID: `{user_id}`\n"
        f"Is Admin: {'✅ Yes' if is_admin_user else '❌ No'}\n"
        f"Is Forwarded: {'✅ Yes' if is_forwarded else '❌ No'}\n"
        f"Has Photo: {'✅ Yes' if has_photo else '❌ No'}\n"
        f"Has Text: {'✅ Yes' if has_text else '❌ No'}\n"
        f"Has Caption: {'✅ Yes' if has_caption else '❌ No'}\n\n"
    )
    
    if not is_admin_user:
        debug_info += "❌ You are not an admin. Send /setadmin first."
    elif not is_forwarded:
        debug_info += "⚠️ This message is not forwarded. You can:\n1. Forward a post (auto-mailing)\n2. Reply to a message with /mailing"
    else:
        debug_info += "✅ You should be able to mailing! Try forwarding a post."
    
    await update.message.reply_text(debug_info, parse_mode='Markdown')


async def handle_forwarded_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle forwarded messages - mailing to all users who used /start (admin only)"""
    message = update.message
    user_id = update.effective_user.id
    
    # Log for debugging
    logger.info(f"Received message from user {user_id}, forwarded: {message.forward_from or message.forward_from_chat}")
    
    # Check if message is forwarded
    if not (message.forward_from or message.forward_from_chat):
        # Not a forwarded message, ignore
        logger.debug(f"Message from user {user_id} is not forwarded, ignoring")
        return
    
    # Check admin permission
    if not is_admin(user_id):
        await update.message.reply_text(
            "❌ Access denied. Only administrators can mailing messages.\n\n"
            "💡 Tip: If you're the first user, send /setadmin to become an administrator."
        )
        logger.warning(f"Non-admin user {user_id} attempted to mailing")
        return
    
    logger.info(f"Admin {user_id} is mailing a message")
    
    # Load all users
    stats = load_user_stats()
    user_ids = list(set(stats["users"]))
    
    # Exclude admin from mailing list (admin already sees the message)
    user_ids = [uid for uid in user_ids if uid != user_id]
    
    if not user_ids:
        await update.message.reply_text("❌ No users found to mailing to (excluding yourself).")
        return
    
    # Confirm mailing start
    await update.message.reply_text(
        f"📤 Mailing to {len(user_ids)} users...\n"
        f"Please wait..."
    )
    
    success_count = 0
    failed_count = 0
    
    # Extract message content - support multiple message types
    has_photo = message.photo is not None and len(message.photo) > 0
    has_video = message.video is not None
    has_document = message.document is not None
    caption = message.caption  # Caption can exist for photo, video, or document
    text = message.text if not (has_photo or has_video or has_document) else None
    
    logger.info(f"Message type - Photo: {has_photo}, Video: {has_video}, Document: {has_document}, Text: {text is not None}, Caption: {caption is not None}")
    logger.info(f"Message details - photo list: {message.photo}, text: {text[:50] if text else None}")
    
    # Check if we have any content to mailing
    if not (has_photo or has_video or has_document or text):
        await update.message.reply_text(
            "❌ Cannot mailing: Message has no content (photo, video, document, or text).\n\n"
            "Please forward a message with content, or use /mailing command by replying to a message."
        )
        return
    
    # Mailing to all users
    # Priority: Use forward_message to preserve Premium emoji and all formatting
    for target_user_id in user_ids:
        try:
            message_sent = False
            
            # First, try to forward the message (preserves Premium emoji and all formatting)
            try:
                await context.bot.forward_message(
                    chat_id=target_user_id,
                    from_chat_id=message.chat_id,
                    message_id=message.message_id
                )
                success_count += 1
                message_sent = True
                logger.info(f"Forwarded message to user {target_user_id} (preserving Premium emoji)")
            except Exception as forward_error:
                # If forwarding fails, fall back to resending (loses Premium emoji but ensures delivery)
                logger.warning(f"Forward failed for user {target_user_id}, trying to resend: {forward_error}")
                
                if has_photo:
                    # Send photo with caption
                    photo = message.photo[-1] if message.photo else None
                    if photo and photo.file_id:
                        await context.bot.send_photo(
                            chat_id=target_user_id,
                            photo=photo.file_id,
                            caption=caption,
                            parse_mode='HTML' if caption else None
                        )
                        success_count += 1
                        message_sent = True
                        logger.info(f"Sent photo to user {target_user_id} (fallback)")
                    else:
                        logger.warning(f"Photo file_id is None for user {target_user_id}")
                elif has_video:
                    # Send video with caption
                    video = message.video
                    if video and video.file_id:
                        await context.bot.send_video(
                            chat_id=target_user_id,
                            video=video.file_id,
                            caption=caption,
                            parse_mode='HTML' if caption else None
                        )
                        success_count += 1
                        message_sent = True
                        logger.info(f"Sent video to user {target_user_id} (fallback)")
                elif has_document:
                    # Send document with caption
                    document = message.document
                    if document and document.file_id:
                        await context.bot.send_document(
                            chat_id=target_user_id,
                            document=document.file_id,
                            caption=caption,
                            parse_mode='HTML' if caption else None
                        )
                        success_count += 1
                        message_sent = True
                        logger.info(f"Sent document to user {target_user_id} (fallback)")
                elif text:
                    # Send text message
                    await context.bot.send_message(
                        chat_id=target_user_id,
                        text=text,
                        parse_mode='HTML'
                    )
                    success_count += 1
                    message_sent = True
                    logger.info(f"Sent text to user {target_user_id} (fallback)")
            
            if not message_sent:
                failed_count += 1
                logger.error(f"Failed to mailing to user {target_user_id}: All methods failed")
                    
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to mailing to user {target_user_id}: {e}", exc_info=True)
    
    # Report results
    result_message = (
        f"📥 Mailing completed!\n\n"
        f"✅ Success: {success_count}\n"
        f"❌ Failed: {failed_count}\n"
        f"📝 Total: {len(user_ids)}"
    )
    await update.message.reply_text(result_message)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Error handler"""
    logger.error(f"Update {update} caused error: {context.error}")


def main():
    """Start Bot"""
    if not BOT_TOKEN:
        logger.error("❗BOT_TOKEN is not set! Please set BOT_TOKEN in .env file")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stats", stat))
    application.add_handler(CommandHandler("setadmin", setadmin))
    application.add_handler(CommandHandler("removeadmin", removeadmin))
    application.add_handler(CommandHandler("listadmins", listadmins))
    application.add_handler(CommandHandler("data", view_data))
    application.add_handler(CommandHandler("mailing", mailing_command))
    application.add_handler(CommandHandler("test_mailing", test_mailing))
    
    # Handle forwarded messages (admin only) - check for forwarded messages first
    # Use a more flexible filter to catch all forwarded messages
    application.add_handler(MessageHandler(
        filters.FORWARDED,
        handle_forwarded_message
    ))
    
    # Handle regular text messages (only if not forwarded and not a command)
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & ~filters.FORWARDED,
        handle_message
    ))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start Bot
    logger.info("Rolex9 Promo Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
