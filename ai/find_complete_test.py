import os
import glob

# 查找 MedGemma 项目中的完整测试脚本
print("Looking for test scripts...")

# 检查常见位置
paths_to_check = [
    r"E:\MedGemma",
    r"E:\MedGemma\scripts",
    r"C:\Users\D",
    r"D:\MedGemma",
]

for base_path in paths_to_check:
    if os.path.exists(base_path):
        print(f"\nChecking: {base_path}")
        for root, dirs, files in os.walk(base_path):
            for f in files:
                if 'test' in f.lower() and f.endswith('.py'):
                    file_path = os.path.join(root, f)
                    # 读取文件大小
                    size = os.path.getsize(file_path)
                    if size > 1000:  # 大于1KB的文件
                        print(f"  {f} ({size} bytes)")
                        # 显示前5行
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as fp:
                                lines = fp.readlines()[:5]
                                print(f"    First lines: {''.join(lines)}")
                        except:
                            pass
