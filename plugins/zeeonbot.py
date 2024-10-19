
# import nest_asyncio
# nest_asyncio.apply()

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import aiohttp
import asyncio
from pyrogram import filters, Client, compose
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait
import re
import threading
import requests
import time
import json
import os, math
from zee5dl  import ZEE5API, Processor
script_directory = os.path.dirname(os.path.abspath("__file__"))

language_order = ['hi', 'ta', 'te', 'kn', 'bn', 'gu', 'pa', 'as', 'or',
                  'ml', 'mr', 'en', 'th', 'ja', 'th', 'id', 'ms', 'ko', 'bho']

# ZEE5API(hevc=True).fetch_episodes_data(1)
# global selected_Video_ids#, selected_Audio_ids
selected_Video_ids = []
selected_Audio_ids = []

app = Client(
    "zee2024",
    api_id = 10755921,
    api_hash = "d5e49fd3637cba407f17807d31c77977",
    # bot_token = "6137898485:AAEzJaeA-K784RS-xN3Q_EzcL_uXA1WkxQA",  # lmc
    bot_token = "1677559691:AAFSzVlg46NhmtNOYdMU08NVuWy6s0KBbYM"  # zee5cc
    )

@app.on_message(filters.command('path') & filters.private )
async def start_command(client, message):
    await message.reply_text(script_directory, quote=True)



@app.on_message(filters.command('dl') & filters.private)# filters.regex(pattern=".*http.*"))
# @app.on_message(filters.private & filters.regex(pattern=".*http.*"))
async def zee5_capture(bot, update):
    # logger.info(update.from_user.id)
    print(update.from_user.id, update.from_user.first_name)
    # await update.reply_text(update.reply_to_message, quote=True)
    imog = await update.reply_text("<b>Processing... ⏳</b>", quote=True)
    link = update.reply_to_message.text #update.text
    contentID = link.split("/")[-1]
    # await imog.edit(text=contentID)
    data, key, baseurl, pssh, filename, subtitle_data, videos_data, audios_data = ZEE5API(hevc=True).extract_streams(contentID)
    # obj = Processor()
    # filename = obj.Processor.final_file_name
    # print("printing",data, key, baseurl, pssh, filename, subtitle_data, videos_data, audios_data)

    # videos_all_data =[(item['width'], item['height'],item['id'], item['codec'], item['bandwidth'], item['video_codec_release_name']) for item in video_details[0]]
    # audios_all_data =[(item['lang'], item['id'], item['audio_codec_release_name'], item['bandwidth_release_name'], item['channels'], item['codec'], item['bandwidth'], item['label'])for item in video_details[1]]
   
    
    videos_datas = [(item['width'], item['height'], item['id'], item['bandwidth'].split(), item['video_codec_release_name']) for item in videos_data]
    videos_data = []
    for video in videos_datas:
        if int(video[1]) >= 240:
            videos_data.append(video)

    audios_data = [(item['lang'], item['id'], item['audio_codec_release_name'], item['bandwidth_release_name'].split(), item['label'])for item in audios_data]
    print("\n\n", videos_data,"\n\n",audios_data)

    SPELL_IMG ="https://graph.org/file/ead67f78d85f79338bdac.jpg"

    Vbuttons = []
    # Create the keyboard using a for loop
    for pos, item in enumerate(videos_data):
        row = [InlineKeyboardButton(text=f"📽️{item[1]}p🎥", callback_data="None")]
        # print(item[4],pos)
        Vbuttons.append(row)
        # sub_buttons
        # sub_callbacks
        # m = []
        sub_rows = []
        sub_row = []
        m = list()
        count= len(item[3])
        print(count)
        for j in range(count):
            # for it in item[3]:
            sub_row.append(InlineKeyboardButton(text=f"{int(item[3][0])//1000}kbps | {item[4]}", callback_data=f"Videoqulity#{item[2]}"))
            print("sub row is ", sub_row)
        # sub_rows.append(sub_row)
        # print("sub rows is ", sub_rows)
        # print("sub row is ", sub_row)
        # sub_rows.append(sub_row)
            # print("sub rows is ", sub_rows)
        if len(sub_row)%2 == 1:  # Check if the last row has only one button
            sub_row.append(InlineKeyboardButton("-", callback_data="None"))
        sub_rows.append(sub_row)
        print("sub rows is ", sub_rows)
        print("sub row  again is ", sub_row)

            # print("sub rows again is ", sub_rows)
        # sub_rows.append(sub_row)
        Vbuttons.extend(sub_rows)
    imog = await imog.edit(text=f"**Select Video Quality For - **`{data['name']}` \n\n**Format :** `bitrate | codec`\n\n**If you Don't seletect Quality in 60s, then highest Quality will be selected** ", reply_markup=InlineKeyboardMarkup(Vbuttons))

    print(selected_Video_ids)
    while True:
        if selected_Video_ids == []:
            await asyncio.sleep(0)
        else:
            break
    print(selected_Video_ids)
    # await imog.delete()
    
    Abuttons = []
    # Create the keyboard using a for loop
    for pos, item in enumerate(audios_data):
        row = [InlineKeyboardButton(text=f"🔊{item[4]}🔊", callback_data="None")]
        # print(item[4],pos)
        Abuttons.append(row)
        # sub_buttons
        # sub_callbacks
        # m = []
        sub_rows = []
        sub_row = []
        m = list()
        count= len(item[3])
        print(count)
        for j in range(count):
            # for it in item[3]:

            audio_dict = {'lang': item[0], 'id': item[1]}
            # audio_dict = [item[0], item[1]]
            print("audio_dict ",audio_dict)
            sub_row.append(InlineKeyboardButton(text=f"{item[3][0]}bps|{item[2]}", callback_data=f"Audioqulity#{json.dumps(audio_dict)}"))
            print("sub row is ", sub_row)
        if len(sub_row)%2 == 1:  # Check if the last row has only one button
            sub_row.append(InlineKeyboardButton("-", callback_data="None"))
        sub_rows.append(sub_row)
        print("sub rows is ", sub_rows)
        print("sub row  again is ", sub_row)

            # print("sub rows again is ", sub_rows)
        # sub_rows.append(sub_row)
        Abuttons.extend(sub_rows)


    # print("\n\n",buttons)

    keyboard_markup = InlineKeyboardMarkup(Abuttons)
    imog = await imog.edit(text=f"**Select Video Quality For - **`{data['name']}` \n\n**Format :** `bitrate | codec`\n\n**If you Don't seletect Quality in 60s, then highest Quality from all Language will be selected** " , reply_markup=keyboard_markup)

    print(selected_Audio_ids)
    while True:
        if selected_Audio_ids == []:
            await asyncio.sleep(0)
        else:
            break
    print(selected_Audio_ids)
    await imog.delete()
    print(f"selected viideo and audio quality is 💞{selected_Video_ids}  {selected_Audio_ids}")
    path_to_finalvideo = Processor(link=data['mpd'], key=key, init_file_name=data['name'], ott=data['ott'], #360p_aa9aeab909e5c454911b5f6a98156e1a
                 baseurl=baseurl, pssh=pssh, filename=filename, subtitle_data=subtitle_data, videos_id=selected_Video_ids[0], audios_id=selected_Audio_ids ).start_process()
    
    selected_Video_ids.clear()
    selected_Audio_ids.clear()
    
    print("final filename is 💚",path_to_finalvideo)
    
    final_directory = os.path.join(script_directory, path_to_finalvideo)
    thumb = get_thumbnail(data['name'], data['image_url'])
    
    imoji = await update.reply_text(text="**Uploading video**", quote=True)
    await bot.send_video(
                    chat_id=update.chat.id,
                    video=final_directory,
                    caption=data['name'],
                    # parse_mode="HTML",
                    duration=data['duration'],
                    # width=width,
                    # height=height,
                    supports_streaming=True,
                    # reply_markup=reply_markup,
                    thumb=thumb,
                    reply_to_message_id=update.reply_to_message_id,
                    # progress=progress_for_pyrogram,progress_args=("upʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....", ms, time.time()),
                    # progress_args=(
                    #     script.UPLOAD_START,
                    #     update.message,
                    #     start_time
                    # )
                )
    await imoji.delete()
    if os.path.isfile(final_directory):
        os.remove(final_directory)
        os.remove(thumb)
        


def get_thumbnail(name, image_url):
    save_path = os.path.join(script_directory, "Thumbnail", f"image.{name}.{time.time()}.jpg")
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return save_path

class callback():
    @app.on_callback_query(filters.regex(r"^Videoqulity#"))
    async def Videoqulity(client: app, query: CallbackQuery):
        _, key = query.data.split("#")
        data = key
        # print(data)
        global selected_Video_ids
        selected_Video_ids.append(data)
        # print(selected_Video_ids)
        

    @app.on_callback_query(filters.regex(r"^Audioqulity#"))
    async def Videoqulity(client: app, query: CallbackQuery):
        _, key = query.data.split("#")
        data = key
        # print(data)
        global selected_Audio_ids
        selected_Audio_ids.append(data)
        # print(selected_Audio_ids)
    

# @Client.on_callback_query()
# async def Videoqulity(client: app, query: CallbackQuery):
#     data = query.data
#     print(data)
#     final_Videoqulity.append(data)
#     return

    # imog = query.message
    # update = query.message.reply_to_message
    # await Bot.send_message(chat_id=query.message.chat.id, text=data)
    # try:
    #     for vid in vidformat:
    #         if data in vid:
    #             # await Bot.send_message(chat_id=query.message.chat.id, text=vid)
    #             global ress
    #             ress = data
    #             global codec
    #             codec = "avc1"
    #     await imog.delete()
    # except Exception as e:
    #     await imog.delete()
    #     await update.reply_text("Couldn't download your video!", quote=True)
    #     print(f"Exception as - {e}")

    # btn1 = [
    #             [
    #                 InlineKeyboardButton(
    #                     text= aud.split('|')[1],
    #                     callback_data=f'Aud#{aud.split("|")[0]}',
    #                 )
    #             ]
    #             for aud in audformat
    #         ]
    # m = await update.reply_text(text="audformat", reply_markup=InlineKeyboardMarkup(btn1), quote=True)
    # return







##########  ###############   ################   ############  ############   ################   ############




class Timer:
    def __init__(self):
        self.timer_thread = None
        self.expired = False

    def start(self, timeout, callback):
        self.expired = False
        self.timer_thread = threading.Timer(timeout, callback)
        self.timer_thread.start()

    def cancel(self):
        if self.timer_thread:
            self.timer_thread.cancel()
            self.expired = True




@app.on_message(filters.private & filters.command(["blkbtn"]))
async def echodot(bot, update):
    videos_data = [('1920', '1080', '1'), ('1280', '720', '2'), ('1024', '576', '3'), ('854', '480', '4'), ('640', '360', '5'), ('428', '240', '6'), ('256', '144', '7'), ('170', '96', '8')]

    audios_data = [('te', '9', 'AAC2.0', ['128K'], 'Telugu'), ('ta', '10', 'AAC2.0', ['128K'], 'Tamil'), ('ml', '11', 'AAC2.0', ['128K'], 'Malayalam'), ('hi', '12', 'AAC2.0', ['128K'], 'Hindi'), ('kn', '13', 'AAC2.0', ['128K'], 'Kannada')]
    
    timer = Timer()

    timer.expired = True
    buttons = []
    # Create the keyboard using a for loop
    for pos, item in enumerate(audios_data):
        row = [InlineKeyboardButton(text=f"🔊{item[4]}🔊", callback_data="None")]
        print(item[4],pos)
        buttons.append(row)
        # sub_buttons
        # sub_callbacks
        # m = []
        sub_rows = []
        sub_row = []
        m = list()
        count= len(item[3])
        print(count)
        for j in range(count):
            # for it in item[3]:
            sub_row.append(InlineKeyboardButton(text=f"{item[3][0]}bps|{item[2]}", callback_data=f"timer#{item[1]}"))
            print("sub row is ", sub_row)
        # sub_rows.append(sub_row)
        # print("sub rows is ", sub_rows)
        # print("sub row is ", sub_row)
        # sub_rows.append(sub_row)
            # print("sub rows is ", sub_rows)
        if len(sub_row)%2 == 1:  # Check if the last row has only one button
            sub_row.append(InlineKeyboardButton("-", callback_data="None"))
        sub_rows.append(sub_row)
        print("sub rows is ", sub_rows)
        print("sub row  again is ", sub_row)

            # print("sub rows again is ", sub_rows)
        # sub_rows.append(sub_row)
        buttons.extend(sub_rows)

    print("\n\n",buttons)

    keyboard_markup = InlineKeyboardMarkup(buttons)
    # timeout_callback = await update.reply_photo(photo="https://graph.org/file/ead67f78d85f79338bdac.jpg", caption="timer", reply_markup=keyboard_markup)

    # Create an Event object
    event = threading.Event()

    # Start a thread that will sleep for 10 seconds
    sleep_thread = threading.Thread(target=sleep_with_cancel, args=(event, 10))
    sleep_thread.start()

    # Wait for the sleep thread to finish or be interrupted
    sleep_thread.join()

    if event.is_set():
        print("The sleep operation was canceled.")
    else:
        print("The sleep operation completed successfully.")

    await update.reply_text("<b>Timer has expired! ... ⏳</b>", quote=True)


def sleep_with_cancel(event, sleep_time):
    print("Starting sleep...")
    for i in range(sleep_time):
        if event.is_set():  # Check if the event is set
            print("Sleep interrupted!")
            return  # Exit the function if interrupted
        time.sleep(1)  # Sleep for 1 second at a time
    print("Finished sleeping!")

lisht = []

@app.on_callback_query(filters.regex(r"^timer#"))
async def Videoqulity(client: app, query: CallbackQuery):
    _, key = query.data.split("#")
    data = key
    print(data)
    lisht.append(data)
    print(lisht)
    timer = Timer()
    timer.cancel()

    return





###########################################################################################################

SPELL_IMG ="https://graph.org/file/ead67f78d85f79338bdac.jpg"
movielist =["A","B","C","D","E","F"]
numlist = [1,2,3,4,5]

@app.on_message(filters.private & filters.command(["blkbtn3"]))
async def echodot(bot, update):

    # Define the main button labels and callback data
    main_button_labels = ["Button 1", "Button 2", "Button 3", "Button 4", "Button 5", "Button 6"]
    main_callback_data = ["main_button1", "main_button2", "main_button3", "main_button4", "main_button5", "main_button6"]

    # Define the sub-button labels and callback data for each row
    sub_button_labels = [["Sub Button 1", "Sub Button 2", "Sub Button 3"],
                        ["Sub Button 4", "Sub Button 5", "Sub Button 6", "Sub Button 7", "Sub Button 8"],
                        ["Sub Button 9", "Sub Button 10"],
                        ["Sub Button 11", "Sub Button 12", "Sub Button 13", "Sub Button 14", "Sub Button 15", "Sub Button 16"],
                        ["Sub Button 17", "Sub Button 18", "Sub Button 19"],
                        ["Sub Button 20", "Sub Button 21", "Sub Button 22", "Sub Button 23", "Sub Button 24"]]
    # for i in sub_button_labels:
    #     if len(i) % 2 == 1:
    #         i.append("-")
    sub_callback_data = [["sub_button1", "sub_button2", "sub_button3", "-"],
                        ["sub_button4", "sub_button5", "sub_button6", "sub_button7", "sub_button8"],
                        ["sub_button9", "sub_button10"],
                        ["sub_button11", "sub_button12", "sub_button13", "sub_button14", "sub_button15", "sub_button16"],
                        ["sub_button17", "sub_button18", "sub_button19"],
                        ["sub_button20", "sub_button21", "sub_button22", "sub_button23", "sub_button24"]]
    # for i in sub_button_labels:
    #     if len(i) % 2 == 1:
    #         i.append("-")
    # print(sub_button_labels)
    # Create a list of buttons

    videos_data = [('1920', '1080', '1'), ('1280', '720', '2'), ('1024', '576', '3'), ('854', '480', '4'), ('640', '360', '5'), ('428', '240', '6'), ('256', '144', '7'), ('170', '96', '8')]

    audios_data = [('te', '9', 'AAC2.0', 'Telugu'), ('ta', '10', 'AAC2.0', 'Tamil'), ('ml', '11', 'AAC2.0', 'Malayalam'), ('hi', '12', 'AAC2.0', 'Hindi'), ('kn', '13', 'AAC2.0', 'Kannada')]
    buttons = []
    

    # Create the keyboard using a for loop
    for i in range(6): 
        row = [InlineKeyboardButton(main_button_labels[i], callback_data=main_callback_data[i])]
        buttons.append(row)
        # print(sub_button_labels[i], len(sub_button_labels[i]))
        # if len(sub_button_labels[i]) % 2 == 1:
        #     print("yes")
        #     sub_buttons = sub_button_labels[i].append("hii")
        # else:
        sub_buttons = sub_button_labels[i]
        # print(sub_buttons)
        sub_callbacks = sub_callback_data[i]
        sub_rows = []
        while sub_buttons:
            sub_row = []
            for j in range(2):
                if sub_buttons:
                    # print(type(sub_buttons))
                    sub_row.append(InlineKeyboardButton(sub_buttons.pop(0), callback_data=sub_callbacks.pop(0)))
                    print(sub_row,"\n\n")
                if len(sub_row)%2 == 1:  # Check if the last row has only one button
                   sub_row.append(InlineKeyboardButton("-", callback_data="None"))
                   print(sub_row,"\n\n")
            sub_rows.append(sub_row)
              # Add a dummy button
        buttons.extend(sub_rows)
    print(buttons)
    # Create a keyboard markup
    keyboard_markup = InlineKeyboardMarkup(buttons)

    # btn = [[InlineKeyboardButton(text=k, callback_data=f"nammuru#{k}")] for k in movielist]
    # btn2 = [[ InlineKeyboardButton(text=num, callback_data=f"nammuru#{num}") for num in numlist] ]
    # btn3 =[[  (InlineKeyboardButton(text=k, callback_data=f"nammuru#{k}"), InlineKeyboardButton(text=num, callback_data=f"nammuru#{num}") )for k in movielist  for num in numlist  ]]
    # btn.append([InlineKeyboardButton(text="Close", callback_data=f'spol##close_spellcheck')])
    # bmtc= [btn, btn2]

    await update.reply_photo(photo=(SPELL_IMG), caption="hello", reply_markup=keyboard_markup)
    # await update.reply_photo(photo=(SPELL_IMG), caption="hello", reply_markup=InlineKeyboardMarkup(btn2))
    # await update.reply_photo(photo=(SPELL_IMG), caption="hello", reply_markup=InlineKeyboardMarkup(btn3))

##############    #################       ###########      #############     ###################   ##################################

SPELL_IMG ="https://graph.org/file/ead67f78d85f79338bdac.jpg"
movielist =["A","B","C","D","E","F"]
numlist = [1,2,3,4,5]

@app.on_message(filters.private & filters.command(["blkbtn2"]))
async def echodot(bot, update):
    # # Define the main button labels and callback data
    # main_button_labels = ["Button 1", "Button 2", "Button 3", "Button 4", "Button 5", "Button 6"]
    # main_callback_data = ["main_button1", "main_button2", "main_button3", "main_button4", "main_button5", "main_button6"]

    # # Define the sub-button labels and callback data
    # sub_button_labels = [["Sub Button 1", "Sub Button 2"], ["Sub Button 3", "Sub Button 4"]]
    # sub_callback_data = [["sub_button1", "sub_button2"], ["sub_button3", "sub_button4"]]

    # # Create a list of buttons
    # buttons = []

    # # Create the keyboard using a for loop
    # for i in range(6):
    #     row = [InlineKeyboardButton(main_button_labels[i], callback_data=main_callback_data[i])]
    #     sub_row = []
    #     for j in range(2):
    #         for k in range(2):
    #             sub_row.append(InlineKeyboardButton(sub_button_labels[j][k], callback_data=sub_callback_data[j][k]))
    #     buttons.append(row)
    #     buttons.append(sub_row)

            ########################## new ######################################
    # buttons = []
    # for i in range(2):  # Create 2 rows
    #     row = []
    #     for j in range(2):  # Create 2 buttons per row
    #         button_text = f"Button {i*2 + j + 1}"
    #         button_callback_data = f"button_{i*2 + j + 1}"
    #         row.append(InlineKeyboardButton(button_text, callback_data=button_callback_data))
    #     buttons.append(row)
    #     if i < 1:  # Add a single button in between rows
    #         single_button_text = f"Single Button {i + 1}"
    #         single_button_callback_data = f"single_button_{i + 1}"
    #         buttons.append([InlineKeyboardButton(single_button_text, callback_data=single_button_callback_data)])


    # # Create a keyboard markup
    # keyboard_markup = InlineKeyboardMarkup(buttons)

######################################### from DRM-Scripts buttons ##############################
    quality_options = ["1080p", "720p", "576p", "480p", "360p", "240p", "144p", "96p"]
    quality_symbols = {
        "Video": "📽",
        "File": "📂",
        "Drive": "☁️"
    }
    buttons = []
    
    for quality in quality_options:
        row = [InlineKeyboardButton(text=f"{quality_symbols[label]}{quality} {label}", callback_data=f"quality_{quality}_{label}") for label in quality_symbols]
        buttons.append(row)

    keyboard_markup = InlineKeyboardMarkup(buttons)


    await update.reply_photo(photo=(SPELL_IMG), caption="hello", reply_markup=keyboard_markup)

############################################################################################################

def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "ᴅ, ") if days else "") + \
        ((str(hours) + "ʜ, ") if hours else "") + \
        ((str(minutes) + "ᴍ, ") if minutes else "") + \
        ((str(seconds) + "ꜱ, ") if seconds else "") + \
        ((str(milliseconds) + "ᴍꜱ, ") if milliseconds else "")
    return tmp[:-2] 

def humanbytes(size):    
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'ʙ'

def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += f"{time_list.pop()}, "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time

PROGRESS_BAR = """<b>\n
╭━━━━❰ᴘʀᴏɢʀᴇss ʙᴀʀ❱━➣
┣⪼ 🗃️ Sɪᴢᴇ: {1} | {2}
┣⪼ ⏳️ Dᴏɴᴇ : {0}%
┣⪼ 🚀 Sᴩᴇᴇᴅ: {3}/s
┣⪼ ⏰️ Eᴛᴀ: {4}
╰━━━━━━━━━━━━━━━➣ </b>"""

async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:        
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "{0}{1}".format(
            ''.join(["⬢" for i in range(math.floor(percentage / 5))]),
            ''.join(["⬡" for i in range(20 - math.floor(percentage / 5))])
        )            
        tmp = progress + PROGRESS_BAR.format( 
            round(percentage, 2),
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),            
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text=f"{ud_type}\n\n{tmp}",               
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]])                                               
            )
        except:
            pass

# audformat = [
# "00:40:26.344 INFO : Aud *CENC audio_hin_2=125375 | 125 Kbps | mp4a.40.2 | hi |",
# "00:40:26.345 INFO : Aud *CENC audio_hin_2=93375 | 93 Kbps | mp4a.40.2 | hi | 2CH",
# "00:40:26.346 INFO : Aud *CENC audio_hin_2=61378 | 61 Kbps | mp4a.40.2 | hi | 2CH",
# "00:40:26.347 INFO : Aud *CENC audio_hin_2=45379 | 45 Kbps | mp4a.40.2 | hi | 2CH"
# ]

# @app.on_callback_query(filters.regex(r"^nammuru#"))
# async def answer(client, callback_query):
# #    h=  await callback_query.answer(
# #         f"A'{callback_query.data}'",
# #         show_alert=True)
# #    print(h)
#     data = callback_query.data
#     print(data)
#     imog = callback_query.message


#     btn1 = [
#                 [
#                     InlineKeyboardButton(
#                         text= aud.split('|')[1],
#                         callback_data=aud.split(': ')[1],
#                         # callback_data=f"lan",
#                     )
#                 ]
#                 for aud in audformat
#             ]
#     m = await imog.edit(text="audformat", reply_markup=InlineKeyboardMarkup(btn1))


# @app.on_callback_query(filters.regex(r"^Aud"))
# async def answer(client, callback_query):
# #    h=  await callback_query.answer(
# #         f"A'{callback_query.data}'",
# #         show_alert=True)
# #    print(h)
#     data = callback_query.data.replace("as#","")
#     print(data)
#     imog = callback_query.message







print("YOUR APP IS LIVE")
app.run()  # Automatically start() and idle()
