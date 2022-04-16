#test.py

import asyncio
import time
import re
import random
import mysqlt

from graia.broadcast import Broadcast

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, Image
from graia.ariadne.model import Friend, MiraiSession, Group, Member

sql = mysqlt.SQL()

loop = asyncio.new_event_loop()

broadcast = Broadcast(loop=loop)
app = Ariadne(
    broadcast=broadcast,
    connect_info=MiraiSession(
        host="http://localhost:8080",  # 填入 HTTP API 服务运行的地址
        verify_key="3258",  # 填入 verifyKey
        account=1759646174,  # 你的机器人的 qq 号
    )
)
bcc = app.broadcast

def judge(string:str):
    t = re.compile("[色|涩]")
    return t.search(string)


broadcast.receiver("FriendMessage")
async def friend_message_listener(app: Ariadne, message:MessageChain, friend: Friend):
    with open("/home/joseph/桌面/yeren_bot/" + str(friend) + ".txt", 'a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S: ", time.localtime()))
        f.write(message.asDisplay())
        f.write("\n")
    sql.saveFriendMessage(friend.id, friend.nickname, message.asDisplay())
    if(judge(str(message))):
        await app.sendMessage(
            friend,
            MessageChain.create(Image(path="/home/joseph/picture/" + str(random.randint(1, 3600)) + ".jpg")),
        )

@bcc.receiver(GroupMessage)
async def setu(app:Ariadne, group:Group, message:MessageChain, member:Member):
    with open("/home/joseph/桌面/yeren_bot/" + str(group) + ".txt", 'a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S: ", time.localtime()))
        f.write(member.name + "(" + str(member.id) + "): ")
        f.write(message.asDisplay())
        f.write("\n")
    sql.saveGroupMessage(group.id, group.name, member.id, member.name, message.asDisplay())

app.launch_blocking()
loop.run_until_complete(app.lifecycle())


