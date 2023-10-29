# -*- coding:utf-8 -*-
"""
@Time : 2022/4/23 8:33 PM
@Author: binkuolo
@Des: views home
"""
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/", summary="门户首页页面", response_class=HTMLResponse)
async def index(request: Request):
    """
    门户首页
    :param request:
    :return:
    """
    return request.app.state.views.TemplateResponse("index.html", {"request": request})
