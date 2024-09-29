#(©)Codexbotz

import aiohttp
import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
from plugins.data import DATAODD, DATAEVEN ,BOTEFITMSG, FOMET
from plugins.cbb import DATEDAY
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON
from datetime import datetime
from helper_func import encode
import requests
import string
import random
import re

# /date commend for set date
@Client.on_message(filters.private & filters.user(ADMINS) & filters.command(["date"]))
async def date(bot, message):
    dat = await message.reply_text("Select your Date.........",quote=True,reply_markup=InlineKeyboardMarkup([[ 
        			InlineKeyboardButton("Yesterday",callback_data='ystdy'), 
        			InlineKeyboardButton("Today",callback_data = 'tdy'), 
        			InlineKeyboardButton("Tommorow",callback_data='tmr') ]]))

@Client.on_message(filters.private & filters.user(ADMINS) & ~filters.text)
async def channel_post(client: Client, message: Message):
    current_time = datetime.now()
    media = message.video or message.document
    
    bot_msg = await message.reply_text("Please Wait...!", quote = True) #reply text please wait... to bot
    try:
        #janvary = current_time.strftime("%B")
        medias = media.file_name.replace(".","_")
        filname = re.split("S\d\d", medias)[0]#[1][2]etc
        Eno= re.findall("S\d+E\d+\d", medias)
        if len(DATEDAY)==0:
            await client.send_message(chat_id=message.chat.id, text="Error: invalid date please set /date")
            bot_msg.delete()
            return 
        else:                
            if int(DATEDAY[-1][0:2]) % 2 != 0:#chaeking for ODD by given date
                if filname in DATAODD.keys(): #matching name in dict key with arrival video file name
                    await asyncio.sleep(1)
                    chtid=int(DATAODD[filname][3])#for particular channel id
                    pic=DATAODD[filname][0] #particuler images
                    SL_URL=DATAODD[filname][1] #for particuler domine name
                    SL_API=DATAODD[filname][2] #for particuler api 
                   # chtid=message.chat.id # if you want pic+formet into bot pm 
                elif filname == "Bigg_Boss_":
                    bot_msg.delete()
                    bigg_boss_S11(client , message)

            elif int(DATEDAY[-1][0:2]) % 2 == 0: #checking for EVEN
                if filname in DATAEVEN.keys():
                    await asyncio.sleep(1)
                    chtid=int(DATAEVEN[filname][3])
                    pic=DATAEVEN[filname][0]
                    SL_URL=DATAEVEN[filname][1]
                    SL_API=DATAEVEN[filname][2]
                    # chtid=message.chat.id # if you want pic+formet into bot pm
                elif filname == "Bigg_Boss_":
                    bot_msg.delete()
                    bigg_boss_S11(client , message)
        
            Size = await get_size(media.file_size)
            await bot_msg.edit("Getting size....!")
            await asyncio.sleep(1)
            Tlink = await conv_link(client , message)
            await bot_msg.edit("Tlink generating....!")
            await asyncio.sleep(1)
            Slink = await get_short(SL_URL, SL_API, Tlink)
            await bot_msg.edit("Slink generating....!")
            await asyncio.sleep(1)
            await bot_msg.edit("Sending post......!")
            await asyncio.sleep(1)
            if Slink:
                await client.send_photo(chat_id=chtid, photo=pic, caption=FOMET.format(DATEDAY[-1], Eno[0], Size, Slink, Slink))
                await bot_msg.edit(BOTEFITMSG.format(filname, Tlink, Slink, Size, DATEDAY[-1])) # msg edit in forwarder channel = "pic without captions (see line 41)" ==> thats return to our given format and short link ,date are updated here
                return 
            else:
                Slink = "ERORR_ACCURED"
                await message.reply_photo(photo=pic, caption=FOMET.format(DATEDAY[-1], Eno[0], Size, Slink, Slink), quote = True)
                await bot_msg.edit(f"<b>Here is your link</b>\n\n<code>{Tlink}</code>\n\n<b>Filename :</b> {medias}")
                return 
    except Exception as e:
        link = await conv_link(client , message)
        await bot_msg.edit(f"<b>Here is your link</b>\n\n{link}\n\n<code>{link}</code>\n\n<b>Exception couse :</b> {e}\n\n<b>Filename :</b> {medias}")
        Slink = "ERORR_ACCURED"
        await message.reply_photo(photo=pic, caption=FOMET.format(DATEDAY[-1], Eno[0], Size, Slink, Slink), quote = True)


@Client.on_message(filters.private & filters.user(ADMINS) & filters.command(["link"]) & ~filters.text)
async def incoming_gen_link(client: Client, message: Message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply('Reply to a message to get a shareable link.')
    file_type = replied.media
    if file_type not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT, enums.MessageMediaType.PHOTO]:
        return await message.reply("**ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ**")
    if message.has_protected_content and message.chat.id not in ADMINS:
        return await message.reply("okDa")
    Tlink = await conv_link(client , replied)
    await message.reply(f"<b>⭕ ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟɪɴᴋ:\n\n🖇️ sʜᴏʀᴛ ʟɪɴᴋ :- {Tlink} \n\n<code>{Tlink}</code></b>")



async def bigg_boss_S11(client , message):
    media = message.video or message.document
    medias = media.file_name.replace(".","_")
    
    Eno= re.findall("S\d+E\d+\d", media)[0]
    quality = re.findall("\d+p", media)[0]
    filname = re.split(Eno, media)
    
    filname = re.split("HS_WEB", filname[1])[0]
    cap = filname.replace("_"," ")
    discript = re.split(quality, cap)[0]

    chtid=int("-1002292058270")
    bot_msg = await message.reply_text("now calling bigg_boss_S11()", quote = True)
    Size = await get_size(media.file_size)
    await bot_msg.edit("Getting size....!")
    await asyncio.sleep(1)
    Tlink = await conv_link(client , message)
    await bot_msg.edit("Tlink generating....!")
    await asyncio.sleep(1)
    Slink = await get_short("adlinkfly.in", "a3f8fd04f9389222dca40c13c17b0d5f69a7e2be", Tlink)
    await bot_msg.edit("Slink generating....!")
    await asyncio.sleep(1)
    await bot_msg.edit("Sending post......!")
    await asyncio.sleep(1)
    if Slink:
        await client.send_photo(chat_id=chtid, photo="https://envs.sh/SsW.jpg", caption=FOMET.format(DATEDAY[-1], Eno, Size, Slink, Slink))
        await bot_msg.edit(BOTEFITMSG.format(discript, Tlink, Slink, Size, DATEDAY[-1])) # msg edit in forwarder channel = "pic without captions (see line 41)" ==> thats return to our given format and short link ,date are updated here
        return
    else:
        Slink = "ERORR_ACCURED"
        await message.reply_photo(photo="https://envs.sh/SsW.jpg", caption=FOMET.format(DATEDAY[-1], cap, Size, Slink, Slink), quote = True)
        await bot_msg.edit(f"<b>Here is your link</b>\n\n<code>{Tlink}</code>\n\n<b>Filename :</b> {medias}")
        return

async def get_short(SL_URL, SL_API, Tlink): #generating short link with particular domine and api
    try:
       api_url = f"https://{SL_URL}/api"
       params = {'api': SL_API, 'url': Tlink}
       async with aiohttp.ClientSession() as session:
           async with session.get(api_url, params=params) as resp:
               data = await resp.json()
               url = data["shortenedUrl"]
       return url
    except:
        resp = requests.get(f"https://{SL_URL}/api?api={SL_API}&url={Tlink}&alias={CustomAlias()}")
        data = resp.json()
        url = data["shortenedUrl"]  
        return url

async def conv_link(client , message):
    try:
       post_message = await message.copy(chat_id = CHANNEL_ID, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id = CHANNEL_ID, disable_notification=True)
    except Exception as e:
        print(e) 
        await client.send_message(message.chat.id, "Somthing is Wrong")
    converted_id = post_message.id * abs(CHANNEL_ID)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    # await client.send_massage(message.chat.id , f"<b>Here is your link</b>\n\n{link}\n\n<code>{link}</code>", disable_web_page_preview = True)
    return link

async def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.1f %s" % (size, units[i])

# @Client.on_message(filters.private & filters.user(ADMINS) & ~filters.text)
# async def channel_post(client: Client, message: Message):
#     Tlink = await conv_link(client , message)
#     bot_msg = await message.reply_text(Tlink, quote = True)


@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):

    if DISABLE_CHANNEL_BUTTON:
        return

    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://telegram.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass


def CustomAlias():
    # Generate a random integer between 3 and 8 (inclusive)
    length = random.randint(3, 8)
    # Define the population of characters to choose from
    population = string.ascii_letters + string.digits
    # Generate a random string of the specified length
    random_string = ''.join(random.choice(population) for _ in range(length))
    return random_string


