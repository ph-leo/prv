#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 get_prompt 函数"""

import re

# 读取文件
f = open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py', 'r', encoding='utf-8')
content = f.read()
f.close()

# 找到函数定义位置
pattern = r'(def get_prompt\(body_part, doctor_diagnosis, use_v74=True\):.*?\"\"\".*?\"\"\"\s+)(body_lower = body_part\.lower\(\)\s+)(# 检测是否为骨折）

replacement = r'''\1body_lower = body_part.lower()
    diagnosis_lower = doctor_diagnosis.lower()
    
    # 根据 doctor_diagnosis 判断病种（新增逻辑，优先级最高）
    fracture_keywords_in_diag = ["骨折", "折", "断", "裂", "粉碎", "塌陷", "压缩", "移位", "骨折?", "断裂", "皮质中断", "骨皮质", "成角", "台阶", "fracture", "break", "crack", "shattered", "comminuted"]
    pulmonary_keywords_in_diag = ["肺炎", "肺不张", "肺气肿", "肺实变", "肺纤维化", "积液", "气胸", "pneumonia", "atelectasis", "emphysema", "consolidation", "fibrosis", "effusion", "pneumothorax"]
    has_fracture_in_diagnosis = any(kw in diagnosis_lower for kw in fracture_keywords_in_diag)
    has_pulmonary_in_diagnosis = any(kw in diagnosis_lower for kw in pulmonary_keywords_in_diag)
    
    # 优先级判断（doctor_diagnosis 优先于 body_part）
    if has_fracture_in_diagnosis and not has_pulmonary_in_diagnosis:
        return FRACTURE_PROMPT_V74, 'fracture'
    if has_pulmonary_in_diagnosis and not has_fracture_in_diagnosis:
        return PULMONARY_PROMPT_V74, 'pulmonary'
    
    # 退回到原来的 body_part 判断逻辑
\2'''

content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

# 写入文件
f = open(r'e:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py', 'w', encoding='utf-8')
f.write(content)
f.close()

print('修改完成！')
