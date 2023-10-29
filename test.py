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

print(str(uuid.uuid1()).replace('-', ''))
print(uuid.uuid3(uuid.NAMESPACE_DNS, "test"))
print(uuid.uuid4()) # b983907d-ab25-4002-9dad-c37968936ba8
print(str(uuid.uuid5(uuid.NAMESPACE_DNS, "test")).replace("-", ""))
