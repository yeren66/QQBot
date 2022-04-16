import asyncio

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

bcc = app.broadcast


# @bcc.receiver(GroupMessage)
# async def setu(app: Ariadne, group: Group, message: MessageChain):
#     await app.sendGroupMessage(
#         group,
#         MessageChain.create(f"不要说{message.asDisplay()}，来点涩图"),
#     )

@broadcast.receiver("FriendMessage")
async def friend_message_listener(app: Ariadne, friend: Friend, message: MessageChain):
    await app.sendMessage(friend, MessageChain.create(Image(path="/home/joseph/picture/" + str(random.randint(1, 3706)) + ".jpg")))
    if(message.asDisplay() == "我要色色"):
        try:
            await app.sendMessage(friend, MessageChain.create(Image(path="/home/joseph/picture/" + str(random.randint(1, 3600)) + ".jpg")))
        except:
            await app.sendMessage(friend, MessageChain.create("色不起来了QAQ"))

    # 实际上 MessageChain.create(...) 有没有 "[]" 都没关系


@broadcast.receiver(NudgeEvent)
async def getup(app: Ariadne, event: NudgeEvent):
    if event.context_type == "group":
        await app.sendGroupMessage(
            event.group_id,
            MessageChain.create("hello~")
        )
    else:
        await app.sendFriendMessage(
            event.friend_id,
            MessageChain.create("别戳我，好痒")
        )


loop.run_until_complete(app.lifecycle())
