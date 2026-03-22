#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 get_prompt 函数 - 添加 doctor_diagnosis 判断逻辑"""

import re

# 读取文件
f = open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py', 'r', encoding='utf-8')
content = f.read()
f.close()

# 找到 get_prompt 函数并修改
# 我们需要在 body_lower = body_part.lower() 后添加 doctor_diagnosis 判断逻辑

# 检查是否已经修改
if 'diagnosis_lower = doctor_diagnosis.lower()' in content:
    print('已经修改过了')
    exit(0)

# 构建新的函数体
old_code = '''def get_prompt(body_part, doctor_diagnosis, use_v74=True):
    """根据身体部位和医生诊断内容选择Prompt"""
    body_lower = body_part.lower()
    
    # 检测是否为骨折（重点优化）
    fracture_keywords = ['''
    
new_code = '''def get_prompt(body_part, doctor_diagnosis, use_v74=True):
    """根据身体部位和医生诊断内容选择Prompt"""
    body_lower = body_part.lower()
    diagnosis_lower = doctor_diagnosis.lower()
    
    # 根据 doctor_diagnosis 判断病种（新增逻辑，优先级最高）
    fracture_keywords_in_diag = [
        '骨折', '折', '断', '裂', '粉碎', '塌陷', '压缩', '移位',
        '骨折?', '断裂', '皮质中断', '骨皮质', '成角', '台阶',
        'fracture', 'break', 'crack', 'shattered', 'comminuted'
    ]
    
    pulmonary_keywords_in_diag = [
        '肺炎', '肺不张', '肺气肿', '肺实变', '肺纤维化', '积液', '气胸',
        'pneumonia', 'atelectasis', 'emphysema', 'consolidation', 'fibrosis',
        'effusion', 'pneumothorax'
    ]
    
    has_fracture_in_diagnosis = any(kw in diagnosis_lower for kw in fracture_keywords_in_diag)
    has_pulmonary_in_diagnosis = any(kw in diagnosis_lower for kw in pulmonary_keywords_in_diag)
    
    # 优先级判断（doctor_diagnosis 优先于 body_part）
    if has_fracture_in_diagnosis and not has_pulmonary_in_diagnosis:
        return FRACTURE_PROMPT_V74, 'fracture'
    
    if has_pulmonary_in_diagnosis and not has_fracture_in_diagnosis:
        return PULMONARY_PROMPT_V74, 'pulmonary'
    
    # 退回到原来的 body_part 判断逻辑
    # 检测是否为骨折（重点优化）
    fracture_keywords = ['''

if old_code in content:
    content = content.replace(old_code, new_code)
    print('替换 old_code 成功')
else:
    print('未找到 old_code')
    # 尝试使用原始代码
    old_code2 = '    # 检测是否为骨折（重点优化）'
    if old_code2 in content:
        # 找到位置插入新代码
        idx = content.find(old_code2)
        new_logic = '''    # 根据 doctor_diagnosis 判断病种（新增逻辑，优先级最高）
    fracture_keywords_in_diag = [
        "骨折", "折", "断", "裂", "粉碎", "塌陷", "压缩", "移位",
        "骨折?", "断裂", "皮质中断", "骨皮质", "成角", "台阶",
        "fracture", "break", "crack", "shattered", "comminuted"
    ]
    
    pulmonary_keywords_in_diag = [
        "肺炎", "肺不张", "肺气肿", "肺实变", "肺纤维化", "积液", "气胸",
        "pneumonia", "atelectasis", "emphysema", "consolidation", "fibrosis",
        "effusion", "pneumothorax"
    ]
    
    has_fracture_in_diagnosis = any(kw in diagnosis_lower for kw in fracture_keywords_in_diag)
    has_pulmonary_in_diagnosis = any(kw in diagnosis_lower for kw in pulmonary_keywords_in_diag)
    
    # 优先级判断（doctor_diagnosis 优先于 body_part）
    if has_fracture_in_diagnosis and not has_pulmonary_in_diagnosis:
        return FRACTURE_PROMPT_V74, 'fracture'
    
    if has_pulmonary_in_diagnosis and not has_fracture_in_diagnosis:
        return PULMONARY_PROMPT_V74, 'pulmonary'
    
    # 退回到原来的 body_part 判断逻辑
    
'''
        content = content[:idx] + new_logic + content[idx:]
        print('直接插入成功')

# 写入文件
f = open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases_opt_20260318.py', 'w', encoding='utf-8')
f.write(content)
f.close()

print('修改完成！文件已保存为 full_test_v7.4_300cases_opt_20260318.py')
