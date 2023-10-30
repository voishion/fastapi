#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 扩展
    Author  : Lu Li (李露)
    File    : exts.py
    Date    : 2023/10/30 11:38
    Site    : https://gitee.com/voishion
    Project : fastapi
"""
from concurrent.futures import ThreadPoolExecutor


async def aiChatThreadPool() -> ThreadPoolExecutor:
    # 创建一个线程池执行器
    return ThreadPoolExecutor(max_workers=4, thread_name_prefix="AiChatThreadPool")
