from telethon import TelegramClient, events, sync

import httpx
import time
import json
import re
import asyncio

# pip3 install telethon pysocks httpx 或者 py -3 -m pip install telethon pysocks httpx

# cookies中间用&分开
cks = "pt_key=AAJgUY9cADDZKiBsnZ7rA3EGI0pX0PJ4jS9zJF3ne9NMtCkdrPs8VhNG3Xy5OOIodyB4YBpim8o;pt_pin=jd_649ec7af1a5ec;&pt_key=AAJgUY6GADD_KnUxJqocHDx21a6ZfGUX8YwSgWQz5wBzd8eJbtkgnDZqggv-0YbZ2NHq8W4YMsU;pt_pin=jd_759107c713cec;&pt_key=AAJgUY8QADC4j7ufZ5sjvwe4QQSEihMIYcRyftJIttRgq8ZoiZpc4DNWAo7FOWbrV6dUGmvCt-A;pt_pin=jd_VwzBlbldMHzJ;"

# url1 = 'https://api.m.jd.com/client.action?functionId=liveDrawLotteryV842&body={"lotteryId":666351,"liveId":3656131}&uuid=8888888&client=apple&clientVersion=9.4.1&st=1615429563038&sign=17c699f8504b22f3e0bf961f7a7d941e&sv=121'

async def send_live(cks, url):
    if len(cks) > 0:
        str_ck = cks.split('&')
        for i in range(1, len(str_ck) + 1):
            if len(str_ck[i - 1]) > 0:
                # print(str_ck[i-1])
                # header
                header = {
                    "user-agent": "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.2(0x18000237) NetType/4G Language/zh_CN",
                    "Referer": "https://servicewechat.com/wx4830b51270836408/13/page-frame.html",
                    "Cookie": str_ck[i - 1],
                }
                # 访问url
                async with httpx.AsyncClient() as client:
                    r = await client.get(url=url, headers=header)
                # r = await httpx.get(url=url, headers=header)
                print(r.text)
                await asyncio.sleep(0.5)



# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
# 必须填写 api_id api_hash proxy
api_id =
api_hash = ''
# 使用代理proxy
# client = TelegramClient('test', api_id, api_hash, proxy=("socks5", '127.0.0.1', 1080))
# 不使用代理
client = TelegramClient('test', api_id, api_hash)

client.start()


async def main():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

    # You can print all the dialogs/conversations that you are part of:
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)

p1 = re.compile(r'[(](.*?)[)]', re.S)

@client.on(events.NewMessage)
async def my_event_handler(event):
    # print(event.raw_text)
    if "看主播" in event.raw_text and "不看主播" in event.raw_text:
        print(event.message.sender_id,event.message.text)
        # if event.message.sender_id == '1663824060':
        sec = re.findall(p1, event.message.text)
        if sec!=None and len(sec)==2:
            await send_live(cks,sec[1])




with client:
    client.loop.run_until_complete(main())
    client.loop.run_forever()
