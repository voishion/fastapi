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
import json
from typing import Any

from fastapi import APIRouter
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketDisconnect

from schemas.base import WebsocketMessage

router = APIRouter()


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
        print(f"客户端IP:{real_ip} 来源:{real_host} ID: {str(u_id)}")
        try:
            await web_socket.accept(subprotocol=None)
            for con in cls.active_connections:
                # 把历史连接移除
                if con["u_id"] == u_id:
                    cls.active_connections.remove(con)
            print(f"客户端IP:{real_ip} 来源:{real_host} ID: {str(u_id)}")
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
            msg = WebsocketMessage(**msg)
            print(f"收到了来自[{msg.user}]的[{msg.action}]消息:[{msg.data}]")
            # 开启异步线程处理问题
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
        print(f"客户端IP:{real_ip} 来源:{real_host} ID: {str(u_id)}")
        await cls.__print_online_num()

    @classmethod
    async def __print_online_num(cls):
        """
        打印当前在线人数
        """
        print(f"当前AiChat在线用户数:{len(cls.active_connections)}")

    @classmethod
    async def send_message(cls,
                           sender: str,
                           sender_type: str,
                           recipient: str,
                           data: dict):
        """
        消息发送
        :param sender: 发送者ID
        :param sender_type: 发送者用户类型
        :param recipient: 接收者用户ID
        :param data: 要发送的数据
        :return: bool，true-发送成功，false-对方不在线
        """
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
                message = json.dumps(structure)
                print(f"主动推送数据:{message}")
                await con["con"].send_text(message)
        if is_online:
            return True
        else:
            return False


router.add_websocket_route('/test', AiChat)
