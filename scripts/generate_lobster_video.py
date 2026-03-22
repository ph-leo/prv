#!/usr/bin/env python3
"""
生成"龙虾在海边跳舞"视频
使用 Hugging Face 免费 API (Stable Video Diffusion)
"""

import requests
import base64
import time
import json

# 提示词
PROMPT = "A cute lobster dancing on a tropical beach at sunset, waves in background, cartoon style, vibrant colors, fun and playful"

# Hugging Face 模型 (免费使用)
MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"

# 注意：Stable Video Diffusion 需要输入图片
# 我们先用 text-to-image 生成一张龙虾图片，然后再转视频

IMAGE_MODEL_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

def generate_image(prompt):
    """生成龙虾图片"""
    print(f"🎨 正在生成图片: {prompt}")
    
    headers = {}  # 免费模式不需要 token
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": 1024,
            "height": 576,
            "num_inference_steps": 25
        }
    }
    
    response = requests.post(IMAGE_MODEL_URL, headers=headers, json=payload)
    
    if response.status_code == 200:
        image_data = response.content
        with open("lobster_image.png", "wb") as f:
            f.write(image_data)
        print("✅ 图片生成成功！已保存为 lobster_image.png")
        return "lobster_image.png"
    else:
        print(f"❌ 图片生成失败: {response.status_code}")
        print(response.text)
        return None

def generate_video(image_path, prompt):
    """从图片生成视频"""
    print(f"🎬 正在生成视频...")
    
    # 读取图片并转 base64
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    # Stable Video Diffusion API
    headers = {}
    
    # 注意：SVD 需要二进制图片数据
    response = requests.post(MODEL_URL, headers=headers, data=image_data)
    
    if response.status_code == 200:
        video_data = response.content
        with open("lobster_dancing.mp4", "wb") as f:
            f.write(video_data)
        print("✅ 视频生成成功！已保存为 lobster_dancing.mp4")
        return "lobster_dancing.mp4"
    else:
        print(f"❌ 视频生成失败: {response.status_code}")
        print(response.text)
        return None

def main():
    print("🦞 龙虾跳舞视频生成器")
    print("=" * 50)
    
    # 步骤 1: 生成龙虾图片
    image_prompt = "A cute cartoon lobster dancing on a tropical beach, sunset, ocean waves, colorful, fun, Pixar style"
    image_path = generate_image(image_prompt)
    
    if not image_path:
        print("\n💡 提示：Hugging Face 免费 API 可能需要排队或速率限制")
        print("   你可以：")
        print("   1. 设置 HF_TOKEN 环境变量获得更好体验")
        print("   2. 访问 https://huggingface.co/spaces 直接使用在线工具")
        return
    
    time.sleep(2)
    
    # 步骤 2: 生成视频
    video_path = generate_video(image_path, PROMPT)
    
    if video_path:
        print("\n🎉 完成！视频已生成:")
        print(f"   图片：{image_path}")
        print(f"   视频：{video_path}")
    else:
        print("\n💡 视频生成可能需要 GPU 支持")
        print("   建议访问 Hugging Face Spaces 在线生成:")
        print("   https://huggingface.co/spaces/stabilityai/stable-video-diffusion")

if __name__ == "__main__":
    main()
