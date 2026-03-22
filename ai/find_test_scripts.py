import os
import glob

# 查找 MedGemma 项目中的测试脚本
print("Looking for test scripts...")

# 检查常见位置
paths_to_check = [
    r"E:\MedGemma",
    r"E:\MedGemma\scripts",
    r"C:\Users\D",
    r"D:\MedGemma",
]

extensions = ['*.py', '*.txt']

for base_path in paths_to_check:
    if os.path.exists(base_path):
        print(f"\nChecking: {base_path}")
        for ext in extensions:
            for file_path in glob.glob(os.path.join(base_path, '**', ext), recursive=True):
                if 'test' in file_path.lower() or 'full' in file_path.lower():
                    print(file_path)
