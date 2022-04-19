import asyncio
import requests
import re
import os

# from graia.application import group
from graia.ariadne.message.parser.twilight import Twilight, FullMatch
from graia.broadcast import Broadcast

from graia.ariadne.app import Ariadne
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend, MiraiSession, Group, Member
from graia.ariadne.event.mirai import NudgeEvent
from datetime import datetime
from graia.ariadne.message.element import At, Plain, Image, Forward, ForwardNode, Quote, Source
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

pat = re.compile(r"测试[0-9]")
judgement_path = ("/home/joseph/桌面/yeren_bot/similarity_judgement/")

@bcc.receiver(GroupMessage)
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if(group.name == "bot测试-(cancel)" and group not in sendobject):
        sendobject.append(group)
    if(group.name == "bot测试2" and group not in sendobject):
        sendobject.append(group)
    if(group.name == "bot测试3" and group not in sendobject):
        sendobject.append(group)
    if(pat.search(group.name)):
        if(message.asDisplay() == "bot"):
            await app.sendMessage(group, MessageChain.create("I'm here"))
        if(message.asDisplay() == "h"):
            await app.sendMessage(group, MessageChain.create("带图片回复1 --> 将图片归类至positive\n带图片回复2 --> 将图片归类至negaive\n带图片回复a --> 将图片归类至archor"))
        pic_id = message[0].id
        choose_id = -1
        for one in message:
            # message总是首先返回一个Source类，用于作为消息的唯一标识
            # 然后按照消息链中的元素返回对应的类
            if isinstance(one, Image):
                # TODO: 这儿有个问题，自己发的消息自己接收不到，因此下面这一串逻辑都没法实现
                # 打算再加一个bot，可能才能实现
                req = requests.get(one.url)
                print(req)
                with open(judgement_path + "raw_picture/" + str(pic_id) + "_" + one.id,'wb') as f:
                    f.write(req.content)
            if isinstance(one, Quote):
                # 这里要实现的需求是获取群里对图片的反馈，并根据反馈将图片从raw中移至positive、negative或archor中
                choose_id = one.id
                # print(choose_id)
            if isinstance(one, Plain) and choose_id != -1:
                pattern = re.compile(f"{choose_id}")
                ret = -1
                if re.search("1", one.asDisplay()):
                    l = os.listdir(judgement_path + "raw_picture/")
                    for i in l:
                        if pattern.search(i):
                            # print(f"cp {judgement_path}raw_picture/{i} {judgement_path}positive_picture/{i}")
                            ret = os.system(f"cp {judgement_path}raw_picture/{i} {judgement_path}positive_picture/{i}")
                            os.remove(f"{judgement_path}raw_picture/{i}")
                            await app.sendMessage(group, MessageChain.create(f"已将{i}归档至positive"))
                elif re.search("2", one.asDisplay()):
                    l = os.listdir(judgement_path + "raw_picture/")
                    for i in l:
                        if pattern.search(i):
                            ret = os.system(f"cp {judgement_path}raw_picture/{i} {judgement_path}negative_picture/{i}")
                            os.remove(f"{judgement_path}raw_picture/i")
                            await app.sendMessage(group, MessageChain.create(f"已将{i}归档至negative"))
                elif re.search("a", one.asDisplay()):
                    l = os.listdir(judgement_path + "raw_picture/")
                    for i in l:
                        if pattern.search(i):
                            ret = os.system(f"cp {judgement_path}raw_picture/{i} {judgement_path}archor_picture/{i}")
                            os.remove(f"{judgement_path}raw_picture/i")
                            await app.sendMessage(group, MessageChain.create(f"已将{i}归档至archor"))
                if ret == -1:
                    await app.sendMessage(group, MessageChain.create(f"未找到含有{choose_id}的图片"))
                    
        return 

    
    if(message.has(Forward)):
        if(len(sendobject) != 0):
            for a in sendobject:
                await app.sendMessage(a, MessageChain.create(message))
    for one in message:
        # if isinstance(one, Source):
        #     print(one.id)
        # if isinstance(one,Quote):
        #     print(one.id)
        if(isinstance(one, Image)):
            # print(one.id)
            pattern = re.compile(f"{one.id}")
            l = os.listdir(judgement_path + "raw_picture/")
            t = 0
            for i in l:
                if pattern.match(i):
                    t = 1
                    break
            if t == 1:
                continue
            req = requests.get(one.url)
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
