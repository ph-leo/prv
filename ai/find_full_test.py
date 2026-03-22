import os

# 查找 full_test 或 medgemma 相关文件
print("Looking for full_test or medgemma files...")

for root, dirs, files in os.walk("C:\\"):
    for f in files:
        if 'full_test' in f.lower() or 'medgemma' in f.lower() or 'prompt' in f.lower():
            print(os.path.join(root, f))
    # 限制总输出
    if sum(1 for f in files if 'full_test' in f.lower() or 'medgemma' in f.lower() or 'prompt' in f.lower()) > 50:
        break
