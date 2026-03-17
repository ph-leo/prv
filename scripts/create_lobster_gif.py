#!/usr/bin/env python3
"""
创建简单的龙虾跳舞动画 GIF
使用 PIL (Pillow)
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_lobster_frame(frame_num, total_frames=30):
    """创建一帧龙虾动画"""
    width, height = 640, 360
    img = Image.new('RGB', (width, height), color=(135, 206, 235))  # 天蓝色背景
    draw = ImageDraw.Draw(img)
    
    # 绘制海滩
    # 沙滩
    draw.rectangle([0, height-80, width, height], fill=(238, 214, 175))  # 沙滩色
    
    # 海浪
    wave_y = height - 100
    for i in range(0, width, 20):
        wave_offset = math.sin((i + frame_num * 10) * 0.05) * 5
        draw.ellipse([i, wave_y + wave_offset, i+25, wave_y + 15 + wave_offset], 
                     fill=(64, 164, 223), outline=(100, 180, 230))
    
    # 太阳
    sun_x = width - 80
    sun_y = 60
    draw.ellipse([sun_x-30, sun_y-30, sun_x+30, sun_y+30], fill=(255, 223, 0))
    
    # 龙虾位置（跳舞动画）
    center_x = width // 2
    base_y = height - 150
    
    # 跳舞动作 - 上下跳动和左右摇摆
    bounce = abs(math.sin(frame_num * 0.3)) * 20
    sway = math.sin(frame_num * 0.4) * 15
    
    lobster_x = center_x + sway
    lobster_y = base_y - bounce
    
    # 绘制龙虾身体（红色椭圆）
    body_color = (220, 20, 60)  # 深红色
    draw.ellipse([lobster_x-40, lobster_y-30, lobster_x+40, lobster_y+50], fill=body_color)
    
    # 龙虾头部
    draw.ellipse([lobster_x-35, lobster_y-50, lobster_x+35, lobster_y-10], fill=body_color)
    
    # 眼睛
    eye_y = lobster_y - 35
    draw.ellipse([lobster_x-20, eye_y-8, lobster_x-8, eye_y+4], fill=(255, 255, 255))
    draw.ellipse([lobster_x+8, eye_y-8, lobster_x+20, eye_y+4], fill=(255, 255, 255))
    draw.ellipse([lobster_x-16, eye_y-5, lobster_x-12, eye_y-1], fill=(0, 0, 0))
    draw.ellipse([lobster_x+12, eye_y-5, lobster_x+16, eye_y-1], fill=(0, 0, 0))
    
    # 触须（摆动动画）
    antenna_wave = math.sin(frame_num * 0.5) * 10
    draw.line([lobster_x-15, lobster_y-45, lobster_x-30+antenna_wave, lobster_y-80], fill=body_color, width=3)
    draw.line([lobster_x+15, lobster_y-45, lobster_x+30-antenna_wave, lobster_y-80], fill=body_color, width=3)
    
    # 大钳子（跳舞动作）
    claw_wave = math.sin(frame_num * 0.6) * 20
    # 左钳子
    draw.ellipse([lobster_x-70, lobster_y-20+claw_wave, lobster_x-40, lobster_y+20+claw_wave], fill=body_color)
    draw.ellipse([lobster_x-80, lobster_y-30+claw_wave, lobster_x-60, lobster_y+10+claw_wave], fill=(255, 100, 100))
    # 右钳子
    draw.ellipse([lobster_x+40, lobster_y-20-claw_wave, lobster_x+70, lobster_y+20-claw_wave], fill=body_color)
    draw.ellipse([lobster_x+60, lobster_y-30-claw_wave, lobster_x+80, lobster_y+10-claw_wave], fill=(255, 100, 100))
    
    # 腿（摆动）
    leg_wave = math.sin(frame_num * 0.8) * 5
    for i in range(4):
        leg_y = lobster_y + 10 + i * 8
        # 左腿
        draw.line([lobster_x-35, leg_y, lobster_x-55, leg_y+15+leg_wave], fill=body_color, width=3)
        # 右腿
        draw.line([lobster_x+35, leg_y, lobster_x+55, leg_y+15-leg_wave], fill=body_color, width=3)
    
    # 尾巴
    tail_wave = math.sin(frame_num * 0.7) * 8
    draw.ellipse([lobster_x-25, lobster_y+45, lobster_x+25, lobster_y+75+tail_wave], fill=body_color)
    draw.ellipse([lobster_x-20, lobster_y+70+tail_wave, lobster_x+20, lobster_y+90+tail_wave], fill=body_color)
    
    # 添加文字
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((width//2-100, 20), "🦞 Lobster Dancing! 🦞", fill=(255, 255, 255), font=font)
    
    return img

def main():
    print("🦞 正在创建龙虾跳舞动画...")
    print("=" * 50)
    
    frames = []
    total_frames = 30
    
    for i in range(total_frames):
        print(f"   生成帧 {i+1}/{total_frames}...")
        frame = create_lobster_frame(i, total_frames)
        frames.append(frame)
    
    # 保存为 GIF
    output_path = "lobster_dancing.gif"
    print(f"\n💾 正在保存 GIF...")
    
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,  # 每帧 100ms
        loop=0
    )
    
    print(f"✅ 动画已生成: {output_path}")
    print(f"📁 完整路径: {os.path.abspath(output_path)}")
    print(f"📊 文件大小: {os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"🎬 帧数: {total_frames}")
    print(f"⏱️  时长: {total_frames * 0.1:.1f} 秒")
    print()
    print("🎉 完成！你可以下载这个 GIF 文件了！")

if __name__ == "__main__":
    main()
