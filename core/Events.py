# -*- coding:utf-8 -*-
"""
@Created on : 2022/4/22 22:02
@Author: binkuolo
@Des: fastapi事件监听
"""
from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from aioredis import Redis
from fastapi import FastAPI

from database.mysql import register_mysql
from database.redis import sys_cache, code_cache
from exts import aiChatThreadPool


def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """

    async def app_start() -> None:
        # APP启动完成后触发
        print("FastAPI已启动")
        # 注册数据库
        await register_mysql(app)
        # 注入缓存到app state
        app.state.cache = await sys_cache()
        app.state.code_cache = await code_cache()
        app.state.aiChatThreadPool = await aiChatThreadPool()

        pass

    return app_start


def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """

    async def stop_app() -> None:
        # APP停止时触发
        print("FastAPI已停止")
        cache: Redis = await app.state.cache
        code: Redis = await app.state.code_cache
        await cache.close()
        await code.close()

        aiChatTP: ThreadPoolExecutor = app.state.aiChatThreadPool
        aiChatTP.shutdown()

    return stop_app
