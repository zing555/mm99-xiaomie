#原作者：happy knva
#精简：@yyfyy123
#增加推送：@vesugier
#多账号推送相关正则参考 @ookamisk

from telethon import TelegramClient, events
import requests, re, time, os

api_id = ''
api_hash = ''
tg_user_id = ''
tg_bot_token = ''
output_msg = True # 是否打印消息
channel_white_list = [1001427039780] # 过滤频道消息
cookies = [
        "",
        ""
        ]

proxies={ #tg推送用代理，不需要的请删除72行proxies参数或者取消73行注释 注释72行
        'http':'http://127.0.0.1:7890',
        'https':'http://127.0.0.1:7890'
        }

regex = re.compile(r"(https://api.m.jd.com.*)\)", re.M)

client = TelegramClient(
        'your session id',
        api_id,
        api_hash
        )

headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
        "Cookie": "",
        }

cookiesRegex = re.compile(r'pt_pin\=(.*?)',re.S)

f = open("push.txt","w")
f.write(" ")
f.close()

def get_bean(url):
    for cookie in cookies:
        headers["Cookie"] = cookie
        pt_pin = re.findall(cookiesRegex, cookie)
        res = requests.get(url, headers=headers).json()
        if int(res['code']) != 0:
            print("cookie无效")
        else:
            print(res['data']['awardTitle'], res['data']['couponQuota'])
        desp = ''
        desp += '账号:【'+pt_pin[0]+'】{} {}\n'.format(res['data']['awardTitle'], res['data']['couponQuota'])
        if "None" in desp:
            continue
        else:
            f=open("push.txt","a")
            f.write(desp)
            f.close

def push():
    print("tg")
    f = open("push.txt","r")
    text = f.read()
    f.close()
    msg ={
        'chat_id': {tg_user_id},
        'text': f'直播间京豆\n\n{text}',
        'disable_web_page_preview': 'true'
        }
    requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendMessage', data=msg, timeout=15,proxies=proxies).json()
    #requests.post(url=f'https://api.telegram.org/bot{tg_bot_token}/sendMessage', data=msg, timeout=15).json()
    f = open("push.txt","w")
    f.write(" ")
    f.close()

@client.on(events.NewMessage(chats=[-1001427039780]))
async def my_event_handler(event):
    # if event.peer_id.channel_id not in channel_white_list :
    #     return
    jdUrl = re.findall(regex, event.message.text)
    count = len(open("push.txt", 'r').readlines())
    if output_msg:
        print(event.message.text)
    if len(jdUrl) == 1:
        get_bean(jdUrl[0])
    if count > 10 :
        push()



with client:
    client.loop.run_forever()
