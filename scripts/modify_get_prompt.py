#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 get_prompt 函数 - 生成优化脚本"""

# 读取原始文件
with open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到 get_prompt 函数并替换
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 查找 get_prompt 函数定义
    if 'def get_prompt(body_part, doctor_diagnosis, use_v74=True):' in line:
        # 复制函数签名
        new_lines.append(line)
        i += 1
        # 复制 docstring
        while i < len(lines) and '"""' not in lines[i]:
            new_lines.append(lines[i])
            i += 1
        if i < len(lines):
            new_lines.append(lines[i])  # 复制结尾的 """
            i += 1
        
        # 添加新的变量定义和判断逻辑
        new_lines.append('    body_lower = body_part.lower()\n')
        new_lines.append('    diagnosis_lower = doctor_diagnosis.lower()\n')
        new_lines.append('\n')
        new_lines.append('    # 根据 doctor_diagnosis 判断病种（新增逻辑，优先级最高）\n')
        new_lines.append('    fracture_keywords_in_diag = [\n')
        new_lines.append('        "骨折", "折", "断", "裂", "粉碎", "塌陷", "压缩", "移位",\n')
        new_lines.append('        "骨折?", "断裂", "皮质中断", "骨皮质", "成角", "台阶",\n')
        new_lines.append('        "fracture", "break", "crack", "shattered", "comminuted"\n')
        new_lines.append('    ]\n')
        new_lines.append('    pulmonary_keywords_in_diag = [\n')
        new_lines.append('        "肺炎", "肺不张", "肺气肿", "肺实变", "肺纤维化", "积液", "气胸",\n')
        new_lines.append('        "pneumonia", "atelectasis", "emphysema", "consolidation", "fibrosis",\n')
        new_lines.append('        "effusion", "pneumothorax"\n')
        new_lines.append('    ]\n')
        new_lines.append('    has_fracture_in_diagnosis = any(kw in diagnosis_lower for kw in fracture_keywords_in_diag)\n')
        new_lines.append('    has_pulmonary_in_diagnosis = any(kw in diagnosis_lower for kw in pulmonary_keywords_in_diag)\n')
        new_lines.append('\n')
        new_lines.append('    # 优先级判断（doctor_diagnosis 优先于 body_part）\n')
        new_lines.append('    if has_fracture_in_diagnosis and not has_pulmonary_in_diagnosis:\n')
        new_lines.append("        return FRACTURE_PROMPT_V74, 'fracture'\n")
        new_lines.append('    if has_pulmonary_in_diagnosis and not has_fracture_in_diagnosis:\n')
        new_lines.append("        return PULMONARY_PROMPT_V74, 'pulmonary'\n")
        new_lines.append('\n')
        new_lines.append('    # 退回到原来的 body_part 判断逻辑\n')
        
        # 跳过原有的判断逻辑，直接找到 has_spine 开始的地方
        while i < len(lines):
            if 'has_spine' in lines[i] and 'spine_keywords' in lines[i-5]:
                # 找到了原有逻辑的开始，跳过这些行直到找到 has_fracture = any
                while i < len(lines) and 'has_fracture = any' not in lines[i]:
                    i += 1
                break
            i += 1
        continue
    
    new_lines.append(line)
    i += 1

# 写入新文件
with open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases_opt_20260318.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print('修改完成！文件已保存为 full_test_v7.4_300cases_opt_20260318.py')
