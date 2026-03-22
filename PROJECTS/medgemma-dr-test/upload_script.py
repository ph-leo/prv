#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过WinSCP批量上传优化脚本到开发电脑
使用前需要:
1. 下载WinSCP命令行工具 (winscp.com)
2. 配置SSH密钥或使用密码
"""

import subprocess
import os
import sys

# 配置
WINSCP_PATH = r"C:\Program Files (x86)\WinSCP\WinSCP.com"
LOCAL_SCRIPT = r"C:\tmp\full_test_v7.4_300cases.py"
REMOTE_SCRIPT = r"/e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py"
SSH_HOST = "127.0.0.1"
SSH_PORT = "12222"
SSH_USER = "D"
SSH_PASSWORD = os.environ.get("SSH_PASSWORD", "your_password_here")

# WinSCP脚本
WINSCP_SCRIPT = f"""
open sftp://{SSH_USER}:{SSH_PASSWORD}@{SSH_HOST}:{SSH_PORT} -hostkey=* 
put "{LOCAL_SCRIPT}" "{REMOTE_SCRIPT}"
close
exit
"""

def upload_script():
    """上传脚本到开发电脑"""
    print("=" * 60)
    print("MedGemma V7.4 优化脚本上传工具")
    print("=" * 60)
    
    # 检查本地文件
    if not os.path.exists(LOCAL_SCRIPT):
        print(f"错误: 本地文件不存在: {LOCAL_SCRIPT}")
        return False
    
    print(f"✓ 本地文件存在: {LOCAL_SCRIPT}")
    print(f"  大小: {os.path.getsize(LOCAL_SCRIPT)} 字节")
    
    # 检查WinSCP
    if not os.path.exists(WINSCP_PATH):
        print(f"\n错误: WinSCP未安装在: {WINSCP_PATH}")
        print("\n请下载WinSCP命令行工具:")
        print("https://winscp.net/eng/download.php")
        return False
    
    print(f"✓ WinSCP找到: {WINSCP_PATH}")
    
    # 询问是否继续
    print("\n" + "=" * 60)
    print("上传配置:")
    print(f"  本地: {LOCAL_SCRIPT}")
    print(f"  远程: {REMOTE_SCRIPT}")
    print(f"  主机: {SSH_HOST}:{SSH_PORT}")
    print("=" * 60)
    
    # 写入WinSCP脚本文件
    script_file = r"C:\tmp\winscp_upload_script.txt"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(WINSCP_SCRIPT)
    
    print(f"\n正在执行上传...")
    print("注意: 请确保WinSCP已配置SSH密钥或密码正确")
    
    try:
        result = subprocess.run(
            [WINSCP_PATH, "/script=" + script_file, "/log=winscp_upload.log"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        print("\n" + "=" * 60)
        if result.returncode == 0:
            print("✓ 上传成功!")
            print("=" * 60)
            print("\n下一步操作:")
            print("1. 在开发电脑执行:")
            print("   cd e:\\ai_test_MedGemma\\ai\\other\\scripts")
            print("   copy full_test_v7.4_300cases.py full_test_v7.4_300cases_backup.py")
            print("\n2. 运行测试:")
            print("   cd e:\\ai_test_MedGemma\\ai\\other")
            print("   python scripts\\full_test_v7.4_300cases.py")
            return True
        else:
            print("✗ 上传失败!")
            print(f"错误: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n✗ 上传超时!")
        return False
    except Exception as e:
        print(f"\n✗ 上传失败: {e}")
        return False

if __name__ == '__main__':
    print("\nMedGemma V7.4 优化脚本上传工具")
    print("=" * 60)
    
    # 读取本地脚本信息
    if os.path.exists(LOCAL_SCRIPT):
        with open(LOCAL_SCRIPT, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"\n本地脚本大小: {len(content)} 字符")
            
            # 检查是否包含优化的Prompt
            if 'FRACTURE_PROMPT_V74' in content:
                print("✓ 包含骨折专用Prompt (FRACTURE_PROMPT_V74)")
            if 'PULMONARY_PROMPT_V74' in content:
                print("✓ 包含肺部专用Prompt (PULMONARY_PROMPT_V74)")
    
    # 执行上传
    print("\n" + "=" * 60)
    success = upload_script()
    
    if not success:
        print("\n" + "=" * 60)
        print("手动上传步骤:")
        print("=" * 60)
        print("\n1. 启动 WinSCP")
        print("2. 连接到:")
