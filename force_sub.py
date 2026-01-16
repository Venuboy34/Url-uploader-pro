from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from config import Config

# Force Subscribe Image
FORCE_SUB_IMAGE = "https://i.ibb.co/pr2H8cwT/img-8312532076.jpg"

async def is_subscribed(client: Client, user_id: int):
    """Check if user is subscribed to the force sub channel"""
    if not Config.FORCE_SUB_CHANNEL:
        return True
    
    try:
        member = await client.get_chat_member(Config.FORCE_SUB_CHANNEL, user_id)
        if member.status in ["creator", "administrator", "member"]:
            return True
        return False
    except UserNotParticipant:
        return False
    except ChatAdminRequired:
        print("⚠️ Bot is not admin in force sub channel!")
        return True
    except Exception as e:
        print(f"Force sub check error: {e}")
        return True

def force_sub_button():
    """Generate force subscribe button"""
    channel_username = Config.FORCE_SUB_CHANNEL_USERNAME
    if not channel_username.startswith("@"):
        channel_username = f"@{channel_username}"
    
    # Remove @ for URL
    channel_link = channel_username[1:]
    
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔔 Join Channel", url=f"https://t.me/{channel_link}")],
        [InlineKeyboardButton("🔄 Try Again", callback_data="check_sub")]
    ])

async def handle_force_sub(client: Client, message):
    """Handle force subscribe check"""
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    if not Config.FORCE_SUB_CHANNEL:
        return True
    
    if await is_subscribed(client, user_id):
        return True
    
    # User not subscribed - send force sub message
    text = f"""👋 **Hello {first_name}!**

⚠️ **You must join our channel to use this bot!**

🔹 Click the **"Join Channel"** button below
🔹 Join the channel
🔹 Click **"Try Again"** to continue

💡 **Why join?**
✅ Get updates about new features
✅ Get notified about bot status
✅ Access exclusive content"""
    
    try:
        await message.reply_photo(
            photo=FORCE_SUB_IMAGE,
            caption=text,
            reply_markup=force_sub_button()
        )
    except:
        await message.reply_text(
            text,
            reply_markup=force_sub_button(),
            disable_web_page_preview=True
        )
    
    return False
