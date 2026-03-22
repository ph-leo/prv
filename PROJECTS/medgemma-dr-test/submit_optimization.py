#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提交优化后的测试脚本到开发电脑
"""

import paramiko
import os
import time

# SSH配置
SSH_HOST = '127.0.0.1'
SSH_PORT = 12222
SSH_USER = 'D'
LOCAL_SCRIPT_PATH = '/tmp/full_test_v7.4_300cases.py'
REMOTE_SCRIPT_PATH = '/e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py'

def upload_script():
    """上传优化后的脚本"""
    print(f'连接到 {SSH_HOST}:{SSH_PORT}...')
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接（需要输入密码或使用密钥）
        # 注意：此处需要手动输入密码，或配置SSH密钥
        
        print(f'\n"===================="')
        print(f'上传优化脚本到开发电脑')
        print(f'"===================="')
        print(f'\n本地文件: {LOCAL_SCRIPT_PATH}')
        print(f'远程文件: {REMOTE_SCRIPT_PATH}')
        print(f'\n请先在开发电脑启动WinSCP或配置SSH密钥')
        print(f'\n或者使用以下命令手动传输:')
        print(f'  scp -P 12222 /tmp/full_test_v7.4_300cases.py D@127.0.0.1:/e/ai_test_MedGemma/ai/other/scripts/')
        print(f'\n上传完成后，在开发电脑执行:')
        print(f'  cd /e/ai_test_MedGemma/ai/other/scripts')
        print(f'  copy full_test_v7.4_300cases.py full_test_v7.4_300cases_backup.py')
        print(f'  copy full_test_v7.4_300cases_v2.py full_test_v7.4_300cases.py')
        print(f'  python full_test_v7.4_300cases.py')
        
    except Exception as e:
        print(f'错误: {e}')

if __name__ == '__main__':
    print('MedGemma V7.4 识别率优化脚本提交工具')
    print('=' * 50)
    
    # 读取优化后的脚本
    if os.path.exists(LOCAL_SCRIPT_PATH):
        print(f'\n读取本地脚本: {LOCAL_SCRIPT_PATH}')
        with open(LOCAL_SCRIPT_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f'脚本大小: {len(content)} 字符')
        
        # 检查是否包含优化的Prompt
        if 'FRACTURE_PROMPT_V74' in content and 'PULMONARY_PROMPT_V74' in content:
            print('✅ 包含优化的骨折和肺部Prompt')
        else:
            print('❌ 未找到优化的Prompt')
    else:
        print(f'错误: 本地脚本不存在: {LOCAL_SCRIPT_PATH}')
    
    print('\n' + '=' * 50)
    print('下一步操作：')
    print('1. 在开发电脑启动WinSCP')
    print('2. 上传 /tmp/full_test_v7.4_300cases.py 到远程')
    print('3. 运行测试验证优化效果')
