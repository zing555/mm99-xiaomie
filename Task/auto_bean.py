from telethon import TelegramClient, events
import requests, re

api_id = '3424893'
api_hash = 'b0319bf481a160fda0e057664fcaa6ff'
output_msg = True # 是否打印消息
channel_white_list = [1427039780] # 过滤频道消息
cookies = [
"pt_key=AAJgNQ3cADC5h47652HLrG_bHCt7XKZppGLCXBmJbMYrunYfEf6M_Ke3rz9K4Kih2HSaE8sJVMw;pt_pin=jd_759107c713cec;&&",
"pt_key=AAJgNRLAADCPOPg9ojF8VP3da_oInF_Bg0tvzCKXlxh7bvH2KPPQDF3Fn8KL22E9NQrRLWMmsNQ;pt_pin=jd_649ec7af1a5ec;",
"pt_key=AAJgNRTFADAfDOKs0Z8-S39zLmowi7RkOpnFbdMqhweEESa2Uz8YtJTpPayxmsFCw2QoJiuDGCw;pt_pin=jd_VwzBlbldMHzJ;"
        ]

regex = re.compile(r"(https://api.m.jd.com.*)\)", re.M)

client = TelegramClient(
        'your session id',
        api_id,
        api_hash,
        proxy=("socks5", '127.0.0.1', 7891) # 代理自行配置或去掉
        )

headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
        "Cookie": "",
        }

def get_bean(url):
    for cookie in cookies:
        headers["Cookie"] = cookie
        res = requests.get(url, headers=headers).json()
        if int(res['code']) != 0:
            print("cookie无效")
        else:
            print(res['data']['awardTitle'], res['data']['couponQuota'])


@client.on(events.NewMessage)
async def my_event_handler(event):
    if event.peer_id.channel_id not in channel_white_list :
        return
    jdUrl = re.findall(regex, event.message.text)
    if output_msg:
        print(event.message.text)
    if len(jdUrl) == 1:
        get_bean(jdUrl[0])

with client:
    client.loop.run_forever()

