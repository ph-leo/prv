#!/usr/bin/env python3
"""
生成"龙虾在海边跳舞"视频
使用 Replicate API (新用户有免费额度) 或 Hugging Face

使用方法:
1. 获取 Replicate token: https://replicate.com/account/api-tokens
2. export REPLICATE_API_TOKEN="your-token"
3. python3 scripts/generate_lobster_video_simple.py
"""

import requests
import os
import time
import json

# 提示词
PROMPT = "A cute cartoon lobster dancing on a tropical beach at sunset, waves in background, vibrant colors, fun and playful, animated style"

def generate_with_replicate(prompt):
    """使用 Replicate API 生成视频 (Zeroscope 模型)"""
    api_token = os.environ.get("REPLICATE_API_TOKEN", "")
    
    if not api_token:
        print("❌ 未设置 REPLICATE_API_TOKEN")
        print("   请访问 https://replicate.com/account/api-tokens 获取 token")
        print("   然后运行：export REPLICATE_API_TOKEN='your-token'")
        return None
    
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    # 创建预测请求
    payload = {
        "version": "9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        "input": {
            "prompt": prompt,
            "num_frames": 24,
            "fps": 8,
            "width": 576,
            "height": 320
        }
    }
    
    print("🎬 正在提交视频生成请求...")
    
    # 创建预测
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json=payload
    )
    
    if response.status_code != 201:
        print(f"❌ 创建预测失败：{response.status_code}")
        print(response.text)
        return None
    
    prediction = response.json()
    prediction_id = prediction["id"]
    print(f"✅ 预测已提交，ID: {prediction_id}")
    
    # 轮询结果
    print("⏳ 正在等待视频生成... (可能需要 1-2 分钟)")
    
    while True:
        time.sleep(5)
        
        status_response = requests.get(
            f"https://api.replicate.com/v1/predictions/{prediction_id}",
            headers=headers
        )
        
        if status_response.status_code != 200:
            print(f"❌ 查询状态失败：{status_response.status_code}")
            return None
        
        status_data = status_response.json()
        status = status_data.get("status", "unknown")
        
        print(f"   当前状态：{status}")
        
        if status == "succeeded":
            video_url = status_data.get("output")
            if video_url:
                print(f"✅ 视频生成成功!")
                print(f"   下载链接：{video_url}")
                
                # 下载视频
                video_response = requests.get(video_url)
                with open("lobster_dancing.mp4", "wb") as f:
                    f.write(video_response.content)
                print("   已保存为：lobster_dancing.mp4")
                return "lobster_dancing.mp4"
            return None
        
        elif status == "failed":
            print(f"❌ 生成失败：{status_data.get('error', 'unknown error')}")
            return None
        
        elif status == "processing":
            continue
        
        else:
            print(f"⚠️ 未知状态：{status}")
            time.sleep(5)

def main():
    print("🦞 龙虾跳舞视频生成器")
    print("=" * 50)
    print(f"提示词：{PROMPT}")
    print()
    
    # 检查是否有 Replicate token
    if os.environ.get("REPLICATE_API_TOKEN"):
        print("使用 Replicate API...")
        video_path = generate_with_replicate(PROMPT)
        
        if video_path:
            print("\n🎉 完成!")
            return
    
    # 如果没有 token，提供替代方案
    print("\n" + "=" * 50)
    print("💡 免费生成方案:")
    print()
    print("1. 【推荐】Hugging Face Spaces (完全免费，无需 API)")
    print("   访问：https://huggingface.co/spaces/stabilityai/stable-video-diffusion")
    print("   输入提示词，直接在线生成")
    print()
    print("2. Replicate (新用户有免费额度)")
    print("   1) 访问：https://replicate.com/account/api-tokens")
    print("   2) 复制 API token")
    print("   3) 运行：export REPLICATE_API_TOKEN='your-token'")
    print("   4) 重新运行此脚本")
    print()
    print("3. 即梦 AI (国内访问快)")
    print("   访问：https://jimeng.jianying.com")
    print("   注册后免费使用")
    print()

if __name__ == "__main__":
    main()
