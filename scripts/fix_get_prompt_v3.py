#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 get_prompt 函数 - 添加 doctor_diagnosis 判断逻辑"""

# 读取文件
f = open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

# 找到 diagnosis_lower 行
diagnosis_line_idx = None
for i, line in enumerate(lines):
    if 'diagnosis_lower = doctor_diagnosis.lower()' in line:
        diagnosis_line_idx = i
        break

if diagnosis_line_idx is None:
    print('未找到 diagnosis_lower 行')
    exit(1)

print(f'找到 diagnosis_lower 行: {diagnosis_line_idx+1}')

# 在 diagnosis_lower 行后插入判断逻辑
new_lines = [
    '    \n',
    '    has_fracture_in_diagnosis = any(kw in diagnosis_lower for kw in fracture_keywords_in_diag)\n',
    '    has_pulmonary_in_diagnosis = any(kw in diagnosis_lower for kw in pulmonary_keywords_in_diag)\n',
    '    \n',
    '    # 优先级判断（doctor_diagnosis 优先于 body_part）\n',
    "    if has_fracture_in_diagnosis and not has_pulmonary_in_diagnosis:\n",
    "        return FRACTURE_PROMPT_V74, 'fracture'\n",
    "    if has_pulmonary_in_diagnosis and not has_fracture_in_diagnosis:\n",
    "        return PULMONARY_PROMPT_V74, 'pulmonary'\n",
    '    \n',
    '    # 退回到原来的 body_part 判断逻辑\n',
]

# 插入新行
lines = lines[:diagnosis_line_idx+1] + new_lines + lines[diagnosis_line_idx+1:]

# 写入文件
f = open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py', 'w', encoding='utf-8')
f.writelines(lines)
f.close()

print('修改完成！')
