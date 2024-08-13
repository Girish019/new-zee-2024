import pandas as pd
import requests
import time


while True:
    
    df=[]
    def send_message():
        bot_id = "6022200330:AAFGVSEpxX0M_jUahlxxVZlQ9xCZvG9D0_4"
        chat_id = int(-1001328262780)
        message = "hii buddy, msg from render for continuous ofter 1 hour"
        url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={message}"

        return requests.get(url).json()


    send_message()
    time.sleep(3600)
    print("ok")
