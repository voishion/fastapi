# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
#     Desc    : 日志配置
#     Author  : Lu Li (李露)
#     File    : logger.py
#     Date    : 2023/10/30 14:32
#     Site    : https://gitee.com/voishion
#     Project : fastapi
# """
# import logging.handlers
# import sys
#
# from config import settings
#
# log_format = "%(asctime)s - %(levelname)s - [%(module)s] - %(funcName)s - [line:%(lineno)d] : %(message)s"
#
# # logging.basicConfig(level=settings.LOG_LEVEL, format=log_format)
#
# log = logging.getLogger()
# log.setLevel(settings.LOG_LEVEL)
# ch = logging.StreamHandler(sys.stdout)
# fh = logging.handlers.RotatingFileHandler("./logs/server.log", mode="a", maxBytes=100 * 1024, backupCount=3)
#
# formatter = logging.Formatter(log_format)
# ch.setFormatter(formatter)
# fh.setFormatter(formatter)
# log.addHandler(ch)  # 将日志输出至屏幕
# log.addHandler(fh)  # 将日志输出至文件
