#(©)CodeXBotz




import os
import logging
from logging.handlers import RotatingFileHandler

Current_File_Path = os.path.abspath(__file__)

#Bot token @Botfather
# TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "1677559691:AAFSzVlg46NhmtNOYdMU08NVuWy6s0KBbYM") #zee
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "6137898485:AAEzJaeA-K784RS-xN3Q_EzcL_uXA1WkxQA") #lmc

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "10755921"))

#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "d5e49fd3637cba407f17807d31c77977")

#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001872633184"))
LOG_ID = int(os.environ.get("LOG_ID", "-1001872633184"))
#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "5636224141"))

#Port
PORT = os.environ.get("PORT", "8080")

#Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Chandan:Chandan@cluster0.2lauy.mongodb.net/cluster0?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot")

#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL = int(os.environ.get("FORCE_SUB_CHANNEL", "-1001872633184"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "15"))

#start message
START_MSG = os.environ.get("START_MESSAGE", "Hello {first}\n\nI can store private files in Specified Channel and other users can access it from special link.")
try:
    ADMINS=[]
    for x in (os.environ.get("ADMINS", "1269341939").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "📁𝐅𝐢𝐥𝐞 𝐍𝐚𝐦𝐞</b> : <code>{filename}</code> \n<b>\n𝐔𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐛𝐲 :- <a href='https://t.me/dot_serials'>𝐃𝐎𝐓 𝐒𝐄𝐑𝐈𝐀𝐋𝐒</a>\n</b>")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "False" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'False'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

ADMINS.append(OWNER_ID)
ADMINS.append(1147676731)
ADMINS.append(1284476297)

LOG_FILE_NAME = "filesharingbot.txt"

LOG_TEXT_P =  """#𝐍𝐞𝐰𝐔𝐬𝐞𝐫

<b>᚛› 𝐈𝐃 - <code>{}</code></b>
<b>᚛› 𝐍𝐚𝐦𝐞 - {}</b>
<b>᚛› 𝐅𝐫𝐨𝐦 -   <a href="https://t.me/Ultra_Reserve_bot">Ultra Stow 🤪</a></b>
"""

RESTART_TXT = """
<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ ! <a href="https://t.me/Ultra_Reserve_bot">Ultra Stow 🤪</a>
📅 Dᴀᴛᴇ : <code>{}</code>
⏰ Tɪᴍᴇ : <code>{}</code>
🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>Asia/Kolkata</code></b>"""

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
