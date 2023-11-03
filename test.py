#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Desc    : 说明
    Author  : Lu Li (李露)
    File    : test.py
    Date    : 2023/10/29 19:36
    Site    : https://gitee.com/voishion
    Project : fastapi
"""
import uuid


from datetime import datetime

time_data = '2023-11-01T00:30'
time_data = '2023-11-01T30:01'
format_string = '%Y-%m-%dT%H:%M'
parsed_time = datetime.strptime(time_data, format_string)


print(parsed_time)

