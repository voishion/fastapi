# -*- coding:utf-8 -*-
"""
@Time : 2022/5/4 10:54 PM
@Author: binkuolo
@Des: 基础schemas
"""
from pydantic import BaseModel, Field
from typing import List, Any, Optional


class BaseResp(BaseModel):
    code: int = Field(description="状态码")
    message: str = Field(description="信息")
    data: List = Field(description="数据")


class ResAntTable(BaseModel):
    success: bool = Field(description="状态码")
    data: List = Field(description="数据")
    total: int = Field(description="总条数")


class WebsocketMessage(BaseModel):
    action: Optional[str]
    user: Optional[int]
    data: Optional[Any]


class AiChatPullMessage(BaseModel):
    """
    AiChat聊天拉取消息schemas类
    """
    action: Optional[str]
    user: Optional[str]
    data: Optional[Any]


# 定义用于接受消息的模型
class AiChatPushMessage(BaseModel):
    """
    AiChat聊天推送消息schemas类
    """
    sender: Optional[str] = Field(description="发送者ID")
    sender_type: Optional[str] = Field(description="发送者用户类型")
    recipient: Optional[str] = Field(description="接收者用户ID")
    message: Optional[str] = Field(description="要发送的数据")


class WechatOAuthData(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    unionid: Optional[str]
    scope: str
    openid: str


class WechatUserInfo(BaseModel):
    openid: str
    nickname: str
    sex: int
    city: str
    province: str
    country: str
    headimgurl: str
    unionid: Optional[str]
