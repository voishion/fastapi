#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : Ai智能聊天
    Author  : Lu Li (李露)
    File    : websocket_aichat.py
    Date    : 2023/10/29 16:57
    Site    : https://gitee.com/voishion
    Project : fastapi
"""
import asyncio
import json
import time
from typing import Any

import jwt
import openai
from fastapi import APIRouter
from jwt import PyJWTError
from pydantic import ValidationError
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketDisconnect

from config import settings
from schemas.base import AiChatPullMessage, AiChatPushMessage

from loguru import logger as log

router = APIRouter()

# openai.api_base = "http://10.133.249.34:8000/v1"
openai.api_base = "https://esb.gt.cn/v1"

openai.api_key = "any"


# 耗时的任务函数
def aichat_process_task(msg: AiChatPullMessage):
    log.info(f"处理来自[{msg.user}]的[{msg.action}]消息:[{msg.data}]")
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
        stream=True,
        headers={
            '_idp_session': 'MTAuMTMzLjY4LjE0NQ%3D%3D%7COGEzNGM5ZjAxNzE1MjVkZjllYTAxNzIwOWVlODkxYTA4YmQwZmE3NGE5NWMxNTJiMDU3NzFkZWM1NjIwODBjOA%3D%3D%7CmvflOeoXJyq9cbkH536tKwvw6Fc%3D'}
    )
    request_time = time.time() - start_time
    t = None
    for i in response:
        # data = i  # type:openai.openai_object.OpenAIObject
        t = time.time()
        # log.info(type(i))
        # log.info(json.dumps(i))
        if "content" in i.choices[0].delta:
            aichat_process_msg_push(msg.user, str(i.choices[0].delta.content))
    tts = t - start_time
    ats = tts - request_time
    log.error(f'AiChatGPT回答结束，总耗时:{tts:.2f} s，请求耗时:{request_time:.2f} s，回答耗时:{ats:.2f} s')


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


def aichat_check_token(token: str):
    """
    AiChat用户验证
    :param token:
    :return:
    """
    try:
        # token解密
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload:
            # 用户ID
            uid = payload.get("user_id", "NULL")
            if uid == 'NULL':
                return False
        else:
            return False
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False
    except (PyJWTError, ValidationError):
        return False
    return uid


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
        u_type = web_socket.query_params.get("u_type")
        token = web_socket.headers.get("sec-websocket-protocol")
        real_ip = web_socket.headers.get('x-forwarded-for')
        real_host = web_socket.headers.get("host")
        try:
            if not u_type or not token:
                raise WebSocketDisconnect
            u_id = aichat_check_token(token)
            if not u_id:
                raise WebSocketDisconnect
            await web_socket.accept(subprotocol=token)

            for con in cls.active_connections:
                # 把历史连接移除
                if con["u_id"] == u_id:
                    cls.active_connections.remove(con)
            log.error(f"接入连接>>>客户端IP:{real_ip} 来源:{real_host} ID: {str(u_id)}")
            # 加入新连接
            cls.active_connections.append({
                "u_id": str(u_id),
                "con": web_socket
            })
            await cls.__print_online_num()
        except WebSocketDisconnect:
            await web_socket.close()
            await cls.__print_online_num()
            log.error("断开了连接")

    # WebSocket 消息接收
    @classmethod
    async def on_receive(cls, web_socket: WebSocket, msg: Any):
        try:
            msg = AiChatPullMessage(**msg)
            log.error(f"收到了来自[{msg.user}]的[{msg.action}]消息:[{msg.data}]")
            # 开启异步线程处理问题
            web_socket.app.state.aiChatThreadPool.submit(aichat_process_task, msg)
        except Exception as e:
            log.error(e)

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
        log.error(f"丢失连接<<<客户端IP:{real_ip} 来源:{real_host} ID: {str(u_id)}")
        await cls.__print_online_num()

    @classmethod
    async def __print_online_num(cls):
        """
        打印当前在线人数
        """
        log.info(f"当前AiChat在线用户数:{len(cls.active_connections)}")

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
                await con["con"].send_text(content)
        if is_online:
            return True
        else:
            return False


router.add_websocket_route('/test', AiChat)
