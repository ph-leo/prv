import os

# 查找 MedGemma 项目
print("Looking for MedGemma projects...")

# 检查常见位置
paths_to_check = [
    r"C:\Users\D\ai",
    r"C:\Users\D\Desktop\python",
    r"C:\Users\D\Documents",
]

for path in paths_to_check:
    if os.path.exists(path):
        print(f"Checking: {path}")
        for root, dirs, files in os.walk(path):
            for f in files:
                if 'prompt' in f.lower() or 'medgemma' in f.lower():
                    print(os.path.join(root, f))
            for d in dirs:
                if 'medgemma' in d.lower() or 'dr' in d.lower():
                    print(os.path.join(root, d))
