#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉消息发送工具 - 使用dingtalk-sdk
"""

import requests
import json
import time
from datetime import datetime

# 钉钉机器人配置
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send"
ACCESS_TOKEN = "openclaw_secure_token_2026"

def send_to_dingtalk(message, chat_id=None):
    """
    发送消息到钉钉群
    
    Args:
        message: 消息内容
        chat_id: 群聊ID（可选）
    
    Returns:
        dict: API响应
    """
    try:
        # 构建请求头
        headers = {
            'Content-Type': 'application/json'
        }
        
        # 构建消息体
        payload = {
            "msgtype": "text",
            "text": {
                "content": message
            },
            "at": {
                "isAtAll": False
            }
        }
        
        # 如果指定了chat_id，添加到URL中
        url = f"{DINGTALK_WEBHOOK}?access_token={ACCESS_TOKEN}"
        
        # 发送请求
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        print(f"发送结果: {result}")
        return result
        
    except Exception as e:
        print(f"发送失败: {e}")
        return {"error": str(e)}


def send_markdown_to_dingtalk(title, markdown_text, chat_id=None):
    """
    发送Markdown消息到钉钉群
    
    Args:
        title: 消息标题
        markdown_text: Markdown格式的正文
        chat_id: 群聊ID（可选）
    
    Returns:
        dict: API响应
    """
    try:
        # 构建请求头
        headers = {
            'Content-Type': 'application/json'
        }
        
        # 构建消息体
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": markdown_text
            },
            "at": {
                "isAtAll": False
            }
        }
        
        # 如果指定了chat_id，添加到URL中
        url = f"{DINGTALK_WEBHOOK}?access_token={ACCESS_TOKEN}"
        
        # 发送请求
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        result = response.json()
        
        print(f"发送结果: {result}")
        return result
        
    except Exception as e:
        print(f"发送失败: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    # 测试发送
    test_msg = "【测试】钉钉发送工具正常工作！"
    result = send_to_dingtalk(test_msg)
    print(f"测试结果: {result}")
