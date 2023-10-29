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

router = APIRouter()


@router.get("/chat", tags=["AiChat"], response_class=HTMLResponse)
async def chat(request: Request):
    """
    AiChat
    :param request:
    :return:
    """
    return request.app.state.views.TemplateResponse("chat/chat.html", {"request": request})
