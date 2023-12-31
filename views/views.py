# -*- coding:utf-8 -*-
"""
@Time : 2022/4/23 11:46 AM
@Author: binkuolo
@Des: 视图路由
"""
from fastapi import APIRouter
from views.viewpoints import home, chat

views_router = APIRouter()

views_router.include_router(home.router, tags=["门户首页"])
views_router.include_router(chat.router, tags=["AiChat"])

