#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : Ai智能聊天
    Author  : Lu Li (李露)
    File    : chat.py
    Date    : 2023/10/29 16:57
    Site    : https://gitee.com/voishion
    Project : fastapi
"""
import asyncio
import json
import time
from typing import Any

import openai
from fastapi import APIRouter
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketDisconnect

from schemas.base import AiChatPullMessage, AiChatPushMessage

router = APIRouter()

openai.api_base = "http://10.133.249.34:8000/v1"
openai.api_key = "any"


# 耗时的任务函数
def aichat_process_task(msg: AiChatPullMessage):
    print(f"处理来自[{msg.user}]的[{msg.action}]消息:[{msg.data}]")
    time.sleep(1)
    start_time = time.time()
    # OpenAI API参数详解
    # https://blog.csdn.net/watson2017/article/details/129055329
    response = openai.ChatCompletion.create(
        model="chatglm2-6b",
        messages=[
            {"role": "system", "content": ""},
            {"role": "user", "content": msg.data}
        ],
        max_tokens=1024,
        temperature=0.75,
        stream=True
    )
    response_time = time.time()
    print(f'请求耗时：{response_time - start_time:.2f} s')
    t = None
    for i in response:
        # data = i  # type:openai.openai_object.OpenAIObject
        t = time.time()
        # print(type(i))
        # print(json.dumps(i))
        if "content" in i.choices[0].delta:
            aichat_process_msg_push(msg.user, str(i.choices[0].delta.content))
    print(f'\n总耗时： {t - start_time:.2f} s')
    print("===结束===")


def aichat_process_msg_push(user_id: str, msg: str):
    """
    AiChat处理结果消息推送
    """
    pushMsg = AiChatPushMessage
    pushMsg.sender = 'aichat'
    pushMsg.sender_type = 'aichat'
    pushMsg.recipient = user_id
    pushMsg.message = msg
    # 同步函数中调用异步函数
    asyncio.run(AiChat.send_message(pushMsg))


class AiChat(WebSocketEndpoint):
    """
    AiChat聊天类
    """

    encoding = "json"
    active_connections = []
    """
    活动websocket链接，[{'u_id':'4658463274544865373', 'con':web_socket}]
    """

    # 单例实例对象
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(AiChat, cls).__new__(cls)
        return cls.__instance

    # WebSocket 连接
    @classmethod
    async def on_connect(cls, web_socket: WebSocket):
        u_id = web_socket.query_params.get("u_id")
        real_ip = web_socket.headers.get('x-forwarded-for')
        real_host = web_socket.headers.get("host")
        try:
            await web_socket.accept(subprotocol=None)
            for con in cls.active_connections:
                # 把历史连接移除
                if con["u_id"] == u_id:
                    cls.active_connections.remove(con)
            print(f"接入连接>>>客户端IP:{real_ip} 来源:{real_host} ID: {str(u_id)}")
            # 加入新连接
            cls.active_connections.append({
                "u_id": str(u_id),
                "con": web_socket
            })
            await cls.__print_online_num()
        except WebSocketDisconnect:
            await web_socket.close()
            print("断开了连接")
            await cls.__print_online_num()

    # WebSocket 消息接收
    @classmethod
    async def on_receive(cls, web_socket: WebSocket, msg: Any):
        try:
            msg = AiChatPullMessage(**msg)
            print(f"收到了来自[{msg.user}]的[{msg.action}]消息:[{msg.data}]")
            # 开启异步线程处理问题
            web_socket.app.state.aiChatThreadPool.submit(aichat_process_task, msg)
        except Exception as e:
            print(e)

    # WebSocket 连接断开
    @classmethod
    async def on_disconnect(cls, web_socket, close_code):
        real_ip = web_socket.headers.get('x-forwarded-for')
        real_host = web_socket.headers.get("host")
        u_id = None
        for con in cls.active_connections:
            if con["con"] == web_socket:
                u_id = con["u_id"]
                # 移除已经断开的连接
                cls.active_connections.remove(con)
        print(f"丢失连接<<<客户端IP:{real_ip} 来源:{real_host} ID: {str(u_id)}")
        await cls.__print_online_num()

    @classmethod
    async def __print_online_num(cls):
        """
        打印当前在线人数
        """
        print(f"当前AiChat在线用户数:{len(cls.active_connections)}")

    @classmethod
    async def send_message(cls, message):
        """
        消息发送
        :param message: AiChat聊天推送消息
        :return: True-发送成功，False-对方不在线
        """

        sender = message.sender
        sender_type = message.sender_type
        recipient = message.recipient
        data = {'content': message.message}

        is_online = False  # 用户在线状态
        for con in cls.active_connections:
            # 找到到对方
            if con["u_id"] == recipient:
                is_online = True
                structure = {
                    "sender": sender,
                    "sender_type": sender_type,
                    "data": data
                }
                content = json.dumps(structure)
                # print(f"主动推送数据:{content}")
                await con["con"].send_text(content)
        if is_online:
            return True
        else:
            return False


router.add_websocket_route('/test', AiChat)
