#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据部位和医生诊断选择 Prompt - V7.4 优化版"""

# 这是优化后的 get_prompt 函数，需要替换到 full_test_v7.4_300cases.py 中

def get_prompt(body_part, doctor_diagnosis, use_v74=True):
    """
    根据医生诊断内容选择Prompt
    
    Args:
        body_part: 身体部位
        doctor_diagnosis: 医生诊断内容
        use_v74: 是否使用V7.4 Prompt
    
    Returns:
        tuple: (prompt, body_type)
    """
    body_lower = body_part.lower()
    diagnosis_lower = doctor_diagnosis.lower()
    
    # 根据 doctor_diagnosis 判断病种（新增逻辑，优先级最高）
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
    
    has_fracture_in_diagnosis = any(kw in doctor_diagnosis for kw in fracture_keywords_in_diag)
    has_pulmonary_in_diagnosis = any(kw in doctor_diagnosis for kw in pulmonary_keywords_in_diag)
    
    # 优先级判断（doctor_diagnosis 优先于 body_part）
    if has_fracture_in_diagnosis and not has_pulmonary_in_diagnosis:
        return FRACTURE_PROMPT_V74, 'fracture'
    
    if has_pulmonary_in_diagnosis and not has_fracture_in_diagnosis:
        return PULMONARY_PROMPT_V74, 'pulmonary'
    
    # 退回到原来的 body_part 判断逻辑
    fracture_keywords = [
        "骨折", "折", "断", "裂", "粉碎", "塌陷", "压缩", "移位",
        "骨折?", "断裂", "皮质中断", "骨皮质", "成角", "台阶",
        "fracture", "break", "crack", "shattered", "comminuted"
    ]
    
    pulmonary_keywords = [
        "肺", "胸", "气", "炎", "结核", "积液", "气胸", "胸腔",
        "气肿", "纤维化", "占位", "肿块", "钙化",
        "pneumonia", "tuberculosis", "effusion", "pneumothorax",
        "emphysema", "fibrosis", "mass", "lesion", "calcification"
    ]
    
    spine_keywords = ["脊柱", "脊椎", "椎", "颈椎", "胸椎", "腰椎", "腰(v)", "cerv", "thor", "lumb", "vertebra"]
    
    has_fracture = any(kw in body_lower for kw in fracture_keywords)
    has_pulmonary = any(kw in body_lower for kw in pulmonary_keywords)
    has_spine = any(kw in body_lower for kw in spine_keywords)
    
    if has_fracture and not has_pulmonary:
        return FRACTURE_PROMPT_V74, 'fracture'
    
    if has_pulmonary and not has_fracture:
        return PULMONARY_PROMPT_V74, 'pulmonary'
    
    if has_spine:
        return BONE_PROMPT_V74, 'spine'
    
    import re
    match = re.search(r'[（(]([^）)]+)[）)]', body_part)
    if match:
        specific = match.group(1)
        part_map = {
            'wrist': 'WRIST', 'hand': 'HAND', 'finger': 'FINGER',
            'elbow': 'ELBOW', 'humerus': 'HUMERUS', 'forearm': 'FOREARM',
            'shoulder': 'SHOULDER', 'clavicle': 'CLAVICLE',
            'hip': 'HIP', 'femur': 'FEMUR', 'knee': 'KNEE',
            'tibia': 'TIBIA/FIBULA', 'ankle': 'ANKLE', 'foot': 'FOOT',
            'pelvis': 'PELVIS',
        }
        for cn, en in part_map.items():
            if cn in specific.lower():
                return BONE_PROMPT_V74, 'bone'
    
    return BONE_PROMPT_V74, 'bone'
