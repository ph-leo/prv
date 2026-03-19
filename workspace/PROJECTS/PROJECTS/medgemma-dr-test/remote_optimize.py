#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程连接开发电脑修改 MedGemma 测试脚本 - 简化版本
"""
import subprocess
import os
import tempfile

def main():
    print("=" * 70)
    print("远程连接开发电脑修改 MedGemma 测试脚本")
    print("=" * 70)
    
    # 1. 连接测试
    print("\n[1/4] 连接测试...")
    r = subprocess.run('ssh -p 12222 D@127.0.0.1 "echo OK"', shell=True, capture_output=True, text=True, errors='ignore')
    print(r.stdout.strip())
    
    # 2. 备份脚本
    print("\n[2/4] 备份脚本...")
    r = subprocess.run('ssh -p 12222 D@127.0.0.1 "cp /e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py /e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases_backup.py 2>&1"', shell=True, capture_output=True, text=True, errors='ignore')
    print("备份完成")
    
    # 3. 创建本地临时文件
    print("\n[3/4] 创建本地临时脚本...")
    local_script = "/tmp/optimize_prompt.py"
    script_content = r'''import re
from pathlib import Path

# 读取原始脚本
orig = Path(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases_backup.py')
out = Path(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py')

code = open(orig, 'r', encoding='utf-8', errors='ignore').read()

# 添加 Prompt 常量定义
prompt_constants = '''
# 骨折识别专用Prompt V7.4
FRACTURE_PROMPT_V74 = """# 骨折识别专用Prompt V7.4

1. 骨皮质连续性检查
   - 必须逐段检查骨皮质是否连续
   - 寻找骨皮质断裂、不连续、移位
   - 关注小骨骼的细微骨折线

2. 高风险漏诊骨折提醒
   - 隐匿性骨折（骨皮质完整但骨小梁紊乱）
   - 应力性骨折（骨皮质外 bị 但骨小梁断裂）
   - 嵌插性骨折（假性骨折线）

3. 详细检查清单
   上肢: 肩胛骨/锁骨/肱骨/桡骨/尺骨/手骨
   下肢: 髋骨/股骨/髌骨/胫骨/腓骨/足骨
   脊柱: 颈椎/胸椎/腰椎/骶椎/尾椎

4. 强制报告格式
   部位: ___
   类型: ___
   程度: ___
   移位: ___
   并发症: ___
"""

# 肺部病变识别专用Prompt V7.4
PULMONARY_PROMPT_V74 = """# 肺部病变识别专用Prompt V7.4

1. 肺野是否清晰
2. 肺纹理是否增粗、紊乱
3. 肺门是否增大、模糊

4. 病变分类
   - 肺炎: 细菌性/病毒性/支原体/真菌性
   - 肺不张: 完全性/不完全性
   - 肺气肿: 弥漫性/局限性
   - 肺实变: 病理性密度增高

5. 特征描述
   - 位置: ___
   - 性质: ___
   - 大小: ___
   - 密度: ___
   - 边界: ___
   - 分布: ___

6. 强制报告格式
   部位: ___
   性质: ___
   大小: ___
   密度: ___
   边界: ___
   伴随征象: ___
"""
'''

    # 插入 Prompt 常量
    insert_marker = "# ==================== 扩展映射规则 V7.4 ===================="
    if insert_marker in code:
        code = code.replace(insert_marker, prompt_constants + "\n" + insert_marker)
    
    # 修改 get_prompt 函数
    old_func = "def get_prompt(body_part):"
    new_func = "def get_prompt(body_part, use_v74=True):"
    code = code.replace(old_func, new_func)
    
    # 修改 prompt 选择逻辑
    old_logic = "body_lower = body_part.lower()\n    if any(kw in body_lower for kw in ["
    new_logic = '''body_lower = body_part.lower()
    if use_v74:
        # 骨折关键词
        if any(kw in body_lower for kw in ['骨折', '断裂', '骨皮质']):
            return FRACTURE_PROMPT_V74, 'fracture'
        # 肺部关键词
        if any(kw in body_lower for kw in ['肺', '胸', '支气管', '肺炎']):
            return PULMONARY_PROMPT_V74, 'pulmonary'
    if any(kw in body_lower for kw in [''']
    
    code = code.replace(old_logic, new_logic)
    
    # 写入新脚本
    open(out, 'w', encoding='utf-8').write(code)
    print("✅ 脚本修改完成")
    print(f"   - 骨折 Prompt: {prompt_constants.count('FRACTURE_PROMPT_V74')} 个")
    print(f"   - 肺部 Prompt: {prompt_constants.count('PULMONARY_PROMPT_V74')} 个")
'''

    with open(local_script, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 4. 上传并执行脚本
    print("\n[4/4] 上传并执行脚本...")
    
    # 上传脚本
    r = subprocess.run(
        f'scp -P 12222 {local_script} D@127.0.0.1:/e/ai_test_MedGemma/ai/other/optimize_prompts.py',
        shell=True, capture_output=True, text=True, errors='ignore'
    )
    
    # 执行脚本
    r = subprocess.run(
        'ssh -p 12222 D@127.0.0.1 "cd /e/ai_test_MedGemma/ai/other && python optimize_prompts.py"',
        shell=True, capture_output=True, text=True, timeout=60, errors='ignore'
    )
    
    if r.stdout:
        print(r.stdout)
    if r.stderr:
        print(f"错误: {r.stderr}")
    
    # 5. 检查结果
    print("\n检查修改结果...")
    r = subprocess.run(
        'ssh -p 12222 D@127.0.0.1 "grep -c FRACTURE_PROMPT_V74 /e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py"',
        shell=True, capture_output=True, text=True, errors='ignore'
    )
    print(f"FRACTURE_PROMPT_V74 出现次数: {r.stdout.strip() if r.stdout else '未找到'}")
    
    r = subprocess.run(
        'ssh -p 12222 D@127.0.0.1 "grep -c PULMONARY_PROMPT_V74 /e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py"',
        shell=True, capture_output=True, text=True, errors='ignore'
    )
    print(f"PULMONARY_PROMPT_V74 出现次数: {r.stdout.strip() if r.stdout else '未找到'}")
    
    # 清理
    os.remove(local_script)
    
    print("\n" + "=" * 70)
    print("✅ 修改完成！")
    print("=" * 70)

if __name__ == '__main__':
    main()
