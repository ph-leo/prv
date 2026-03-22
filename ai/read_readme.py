import sys
import io

# 修正 stdout 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 读取 README 文件
with open(r'E:\MedGemma\README.md', 'r', encoding='utf-8') as f:
    content = f.read()
    print(content[:2000])
