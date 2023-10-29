#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : Ai聊天页面视图
    Author  : Lu Li (李露)
    File    : sss.py
    Date    : 2023/10/29 16:50
    Site    : https://gitee.com/voishion
    Project : fastapi
"""
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from api.endpoints.chat import AiChat
from core.Response import success, fail
from schemas.base import AiChatPushMessage

router = APIRouter()


@router.get("/chat", tags=["AiChat"], response_class=HTMLResponse)
async def chat(request: Request):
    """
    AiChat
    :param request:
    :return:
    """
    return request.app.state.views.TemplateResponse("chat/chat.html", {"request": request})


# 新的HTTP端点用于发送消息
@router.post("/push_msg", tags=["AiChat"], summary="所有角色下拉选项专用")
async def send_message(message: AiChatPushMessage, aiChat=None):
    result = await aiChat.send_message(sender=message.sender, sender_type=message.sender_type,
                                       recipient=message.recipient, data={'content': message.message})
    if result:
        return success(msg="推送成功")
    else:
        return fail(msg="对方不在线")
