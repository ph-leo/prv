#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程连接开发电脑修改 MedGemma 测试脚本 - 最终版本
"""

import subprocess
import sys

def main():
    print("=" * 70)
    print("远程连接开发电脑修改 MedGemma 测试脚本")
    print("=" * 70)
    
    # 修改脚本的 Python 代码（简化版）
    modify_code = r'''import re; from pathlib import Path; orig = Path(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases_backup.py'); out = Path(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py'); fp = """FRACTURE_PROMPT_V74=\"\"\"# 骨折识别专用Prompt
1. 骨皮质连续性检查
2. 寻找骨皮质断裂、不连续、移位
3. 关注小骨骼的细微骨折线
判断该X光片是否显示骨折。如果显示骨折，请详细描述骨折的位置、类型、程度和移位情况。
\"\"\"\"""; pp = """PULMONARY_PROMPT_V74=\"\"\"# 肺部病变识别专用Prompt
1. 肺野是否清晰
2. 肺纹理是否增粗、紊乱
3. 肺门是否增大、模糊
判断该X光片是否显示肺部病变。如果有病变，请详细描述病变的位置、性质、大小和密度特征。
\"\"\"\""""; c = open(orig, 'r', encoding='utf-8').read(); c = c.replace('def get_prompt(body_part):', 'def get_prompt(body_part, use_v74=True):').replace('body_lower = body_part.lower()\n    if any(kw in body_lower for kw in [', f'body_lower = body_part.lower()\n    if use_v74:\n        if any(kw in body_lower for kw in [\'骨折\', \'断裂\', \'骨皮质\']):\n            return FRACTURE_PROMPT_V74, \'fracture\'\n        if any(kw in body_lower for kw in [\'肺\', \'胸\', \'支气管\', \'肺炎\']):\n            return PULMONARY_PROMPT_V74, \'pulmonary\'\n    if any(kw in body_lower for kw in ['); c = c.replace('# ==================== 扩展映射规则 V7.4 ====================', f'{fp}\n{pp}\n# ==================== 扩展映射规则 V7.4 ===================='); open(out, 'w', encoding='utf-8').write(c); print("修改完成")'''
    
    # 1. 连接测试
    print("\n[1/3] 连接测试...")
    r = subprocess.run('ssh -p 12222 D@127.0.0.1 "echo OK"', shell=True, capture_output=True, text=True)
    print(r.stdout.strip())
    
    # 2. 备份脚本
    print("\n[2/3] 备份脚本...")
    r = subprocess.run('ssh -p 12222 D@127.0.0.1 "cp /e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py /e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases_backup.py 2>&1"', shell=True, capture_output=True, text=True)
    print("备份完成")
    
    # 3. 执行修改
    print("\n[3/3] 执行修改...")
    cmd = f'ssh -p 12222 D@127.0.0.1 "python -c \\"{modify_code}\\""'
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
    print(r.stdout)
    if r.stderr:
        print(f"错误: {r.stderr}")
    
    # 4. 检查结果
    print("\n检查修改结果...")
    r = subprocess.run('ssh -p 12222 D@127.0.0.1 "grep -c FRACTURE_PROMPT_V74 /e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py"', shell=True, capture_output=True, text=True)
    print(f"FRACTURE_PROMPT_V74 出现次数: {r.stdout.strip()}")
    r = subprocess.run('ssh -p 12222 D@127.0.0.1 "grep -c PULMONARY_PROMPT_V74 /e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py"', shell=True, capture_output=True, text=True)
    print(f"PULMONARY_PROMPT_V74 出现次数: {r.stdout.strip()}")
    
    print("\n" + "=" * 70)
    print("✅ 修改完成！")
    print("=" * 70)

if __name__ == '__main__':
    main()
