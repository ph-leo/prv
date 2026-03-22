#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""快速修复 get_prompt 函数"""

# 读取文件
f = open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

# 找到并重新组织 get_prompt 函数
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 查找 get_prompt 函数
    if 'def get_prompt(body_part, doctor_diagnosis, use_v74=True):' in line:
        # 保存函数签名
        new_lines.append(line)
        i += 1
        
        # 保存 docstring
        while i < len(lines) and '"""' not in lines[i]:
            new_lines.append(lines[i])
            i += 1
        if i < len(lines):
            new_lines.append(lines[i])  # 复制结尾的 """
            i += 1
        
        # 插入新的函数体
        new_lines.append('    body_lower = body_part.lower()\n')
        new_lines.append('    diagnosis_lower = doctor_diagnosis.lower()\n')
        new_lines.append('\n')
        new_lines.append('    # 根据 doctor_diagnosis 判断病种（新增逻辑，优先级最高）\n')
        new_lines.append('    fracture_keywords_in_diag = [\n')
        new_lines.append('        "骨折", "折", "断", "裂", "粉碎", "塌陷", "压缩", "移位",\n')
        new_lines.append('        "骨折?", "断裂", "皮质中断", "骨皮质", "成角", "台阶",\n')
        new_lines.append('        "fracture", "break", "crack", "shattered", "comminuted"\n')
        new_lines.append('    ]\n')
        new_lines.append('    \n')
        new_lines.append('    pulmonary_keywords_in_diag = [\n')
        new_lines.append('        "肺炎", "肺不张", "肺气肿", "肺实变", "肺纤维化", "积液", "气胸",\n')
        new_lines.append('        "pneumonia", "atelectasis", "emphysema", "consolidation", "fibrosis",\n')
        new_lines.append('        "effusion", "pneumothorax"\n')
        new_lines.append('    ]\n')
        new_lines.append('\n')
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
        
        # 跳过旧代码，直到找到 has_spine 开始的地方
        while i < len(lines):
            if 'spine_keywords = ' in lines[i] or 'has_spine = ' in lines[i]:
                break
            i += 1
        
        # 继续复制剩余代码（从 has_spine 开始）
        continue
    
    new_lines.append(line)
    i += 1

# 写入文件
f = open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py', 'w', encoding='utf-8')
f.writelines(new_lines)
f.close()

print('修复完成！')
