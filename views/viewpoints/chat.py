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
from api.endpoints.websocket_aichat import AiChat
from core.Auth import create_access_token
from loguru import logger as log
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
    jwt_data = {
        "user_id": Utils.random_uuid(),
        "user_type": '1'
    }
    jwt_token = create_access_token(data=jwt_data)
    return request.app.state.views.TemplateResponse("chat/chat.html", {"request": request, "token": jwt_token})


# 新的HTTP端点用于发送消息
@router.post("/push_msg", summary="所有角色下拉选项专用", response_model=BaseResp)
async def send_message(request: Request, message: AiChatPushMessage):
    # 获取请求的头部信息
    request_headers = dict(request.headers)
    # 记录请求头信息到日志
    log.info(f"Request Headers: {request_headers}")
    result = await AiChat.send_message(message)
    if result:
        return success(msg="推送成功")
    else:
        return fail(msg="对方不在线")
