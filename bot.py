import asyncio
import requests

# from graia.application import group
from graia.ariadne.message.parser.twilight import Twilight, FullMatch
from graia.broadcast import Broadcast

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend, MiraiSession, Group, Member
from graia.ariadne.event.mirai import NudgeEvent
from datetime import datetime
from graia.ariadne.message.element import At, Plain, Image, Forward, ForwardNode
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.event.message import  ActiveFriendMessage, ActiveGroupMessage

import random

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

sendobject = []

bcc = app.broadcast

# @bcc.receiver("ActiveFriendMessage")
# async def send(event: ActiveFriendMessage):
#     await app.sendMessage(event.subject, event.messageChain)
    # if(group.name == "bot测试"):
    #     app.sendMessage(group, MessageChain.create("hi~"))
    #     while(len(record) != 0):
    #         app.sendMessage(group, MessageChain.create(record.pop()))
    #     while(len(images) != 0):
    #         app.sendMessage(group, MessageChain.create(images.pops()))


@bcc.receiver(GroupMessage)
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if(group.name == "bot测试-(cancel)" and group not in sendobject):
        sendobject.append(group)
    if(group.name == "bot测试2" and group not in sendobject):
        sendobject.append(group)
    if(group.name == "bot测试3" and group not in sendobject):
        sendobject.append(group)
    if(group.name == "bot测试2" or group.name == "bot测试3"):
        if(message.asDisplay() == "bot"):
            await app.sendMessage(group, MessageChain.create("I'm here"))
        return 

    if(message.has(Forward)):
        if(len(sendobject) != 0):
            for a in sendobject:
                await app.sendMessage(a, MessageChain.create(message))
    if(message.has(Image)):
        image = message.__getitem__(Image)[0]
        req = requests.get(image.url)
        print("size: " + req.headers.get('Content-Length'))
        if(int(req.headers.get('Content-Length')) > 50000):
            if(len(sendobject) != 0):
                for a in sendobject:
                    await app.sendMessage(a, MessageChain.create(message))


@broadcast.receiver("FriendMessage")
async def friend_message_listener(app: Ariadne, friend: Friend, message: MessageChain):
    await app.sendMessage(friend, MessageChain.create("hello"))
    if(message.has(Forward)):
        await app.sendMessage(friend, MessageChain.create(message))


    # 实际上 MessageChain.create(...) 有没有 "[]" 都没关系


# @broadcast.receiver(NudgeEvent)
# async def getup(app: Ariadne, event: NudgeEvent):
#     if event.context_type == "group":
#         await app.sendGroupMessage(
#             event.group_id,
#             MessageChain.create("hello~")
#         )
#     else:
#         await app.sendFriendMessage(
#             event.friend_id,
#             MessageChain.create("别戳我，好痒")
#         )


loop.run_until_complete(app.lifecycle())
# app.launch_blocking()