import os
import subprocess
import sys

# Try to run a Python script on the remote server
script = '''
import os
import glob

# 查找 MedGemma 项目
print("Looking for MedGemma projects...")

# 检查常见位置
paths_to_check = [
    r"C:\\Users\\D\\ai",
    r"C:\\Users\\D\\Desktop\\python",
    r"C:\\Users\\D\\Documents",
    r"C:\\MedGemma",
    r"D:\\MedGemma",
]

for path in paths_to_check:
    if os.path.exists(path):
        print(f"Checking: {path}")
        for root, dirs, files in os.walk(path):
            for f in files:
                if 'prompt' in f.lower() or 'medgemma' in f.lower():
                    print(os.path.join(root, f))
                    
            # 限制输出
            if sum(len(glob.glob(os.path.join(root, p))) for p in ['*prompt*', '*medgemma*']) > 20:
                break
'''

with open('/tmp/check_medgemma.py', 'w') as f:
    f.write(script)

print("Script saved. Waiting for remote execution...")
