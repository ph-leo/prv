#!/usr/bin/env python3
"""
自动使用 Hugging Face 免费 API 生成龙虾视频
无需 token，使用免费推理端点
"""

import requests
import time
import os

# 提示词
PROMPT = "A cute cartoon lobster dancing on a tropical beach at sunset, waves in background, vibrant colors, fun and playful, animated style"

def generate_image_free():
    """使用 Hugging Face 免费 API 生成图片"""
    print("🎨 正在生成龙虾图片...")
    
    # 使用免费的 text-to-image 模型
    # 注意：免费 API 有限制，可能需要等待
    models = [
        "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
        "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
        "https://api-inference.huggingface.co/models/prompthero/openjourney-v4",
    ]
    
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "inputs": PROMPT,
        "parameters": {
            "width": 768,
            "height": 432,
            "num_inference_steps": 25,
            "guidance_scale": 7.5
        }
    }
    
    for model_url in models:
        try:
            print(f"   尝试模型: {model_url.split('/')[-1]}")
            response = requests.post(
                model_url, 
                headers=headers, 
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                # 保存图片
                with open("lobster_image.png", "wb") as f:
                    f.write(response.content)
                print("✅ 图片生成成功！")
                return "lobster_image.png"
            
            elif response.status_code == 503:
                # 模型正在加载
                print(f"   模型正在加载，等待...")
                time.sleep(20)
                # 重试
                response = requests.post(model_url, headers=headers, json=payload, timeout=120)
                if response.status_code == 200:
                    with open("lobster_image.png", "wb") as f:
                        f.write(response.content)
                    print("✅ 图片生成成功！")
                    return "lobster_image.png"
            
            else:
                print(f"   失败: {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                
        except Exception as e:
            print(f"   错误: {e}")
            continue
    
    return None

def generate_video_free(image_path):
    """使用 Hugging Face 免费 API 生成视频"""
    print("🎬 正在生成视频...")
    
    # 读取图片
    with open(image_path, "rb") as f:
        image_data = f.read()
    
    # Stable Video Diffusion 模型
    model_url = "https://api-inference.huggingface.co/models/stabilityai/stable-video-diffusion-img2vid-xt"
    
    try:
        print(f"   调用 Stable Video Diffusion...")
        response = requests.post(
            model_url,
            data=image_data,
            timeout=180
        )
        
        if response.status_code == 200:
            with open("lobster_dancing.mp4", "wb") as f:
                f.write(response.content)
            print("✅ 视频生成成功！")
            return "lobster_dancing.mp4"
        
        elif response.status_code == 503:
            print(f"   模型正在加载，等待 30 秒...")
            time.sleep(30)
            response = requests.post(model_url, data=image_data, timeout=180)
            if response.status_code == 200:
                with open("lobster_dancing.mp4", "wb") as f:
                    f.write(response.content)
                print("✅ 视频生成成功！")
                return "lobster_dancing.mp4"
        
        else:
            print(f"   失败: {response.status_code}")
            print(f"   响应: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"   错误: {e}")
        return None

def main():
    print("🦞 自动龙虾视频生成器")
    print("=" * 60)
    print(f"提示词: {PROMPT}")
    print()
    
    # 步骤 1: 生成图片
    image_path = generate_image_free()
    
    if not image_path:
        print("\n❌ 图片生成失败")
        print("\n可能原因：")
        print("- Hugging Face 免费 API 当前繁忙")
        print("- 模型正在加载中")
        print("- 需要等待队列")
        print("\n建议：稍后重试，或访问 https://huggingface.co/spaces 直接使用")
        return
    
    print(f"\n图片已保存: {image_path}")
    time.sleep(2)
    
    # 步骤 2: 生成视频
    video_path = generate_video_free(image_path)
    
    if video_path:
        print("\n" + "=" * 60)
        print("🎉 成功生成龙虾跳舞视频！")
        print(f"📁 文件位置: {os.path.abspath(video_path)}")
        print(f"📊 文件大小: {os.path.getsize(video_path) / 1024 / 1024:.2f} MB")
        print()
        print("你现在可以下载这个视频文件了！")
    else:
        print("\n❌ 视频生成失败")
        print(f"\n但图片已生成: {image_path}")
        print("你可以用这张图片去其他工具生成视频")

if __name__ == "__main__":
    main()
