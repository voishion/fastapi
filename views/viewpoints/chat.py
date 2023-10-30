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
from core import Utils
from core.Response import success, fail
from schemas.base import AiChatPushMessage, BaseResp

router = APIRouter()


@router.get("/chat", summary="AiChat页面", response_class=HTMLResponse)
async def chat(request: Request):
    """
    AiChat
    :param request:
    :return:
    """
    user_id = Utils.random_uuid()
    return request.app.state.views.TemplateResponse("chat/chat.html", {"request": request, "user_id": user_id})


# 新的HTTP端点用于发送消息
@router.post("/push_msg", summary="所有角色下拉选项专用", response_model=BaseResp)
async def send_message(message: AiChatPushMessage):
    result = await AiChat.send_message(message)
    if result:
        return success(msg="推送成功")
    else:
        return fail(msg="对方不在线")
