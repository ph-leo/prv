#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据 doctor_diagnosis 判断病种类型的逻辑"""

# 根据 doctor_diagnosis 判断病种的逻辑如下：

# 1. 骨折关键词（在 doctor_diagnosis 中查找）
FRACTURE_KEYWORDS = [
    "骨折", "折", "断", "裂", "粉碎", "塌陷", "压缩", "移位",
    "骨折?", "断裂", "皮质中断", "骨皮质", "成角", "台阶",
    "fracture", "break", "crack", "shattered", "comminuted"
]

# 2. 肺部疾病关键词（在 doctor_diagnosis 中查找）
PULMONARY_KEYWORDS = [
    "肺炎", "肺不张", "肺气肿", "肺实变", "肺纤维化", "积液", "气胸",
    "pneumonia", "atelectasis", "emphysema", "consolidation", "fibrosis",
    "effusion", "pneumothorax"
]

# 3. 判断逻辑
def determine_disease_type(doctor_diagnosis):
    """
    根据医生诊断内容判断病种类型
    
    Args:
        doctor_diagnosis: 医生诊断文本
    
    Returns:
        tuple: (prompt_type, body_type)
        - prompt_type: FRACTURE_PROMPT_V74 / PULMONARY_PROMPT_V74 / BONE_PROMPT_V74
        - body_type: 'fracture' / 'pulmonary' / 'bone'
    """
    diagnosis_lower = doctor_diagnosis.lower()
    
    # 检查是否包含骨折关键词
    has_fracture = any(kw in doctor_diagnosis for kw in FRACTURE_KEYWORDS)
    
    # 检查是否包含肺部疾病关键词
    has_pulmonary = any(kw in doctor_diagnosis for kw in PULMONARY_KEYWORDS)
    
    # 优先级判断
    if has_fracture and not has_pulmonary:
        return "FRACTURE_PROMPT_V74", "fracture"
    
    if has_pulmonary and not has_fracture:
        return "PULMONARY_PROMPT_V74", "pulmonary"
    
    # 如果两种都没有明确指示，返回 bone（作为 fallback）
    return "BONE_PROMPT_V74", "bone"


# 测试用例
if __name__ == "__main__":
    test_cases = [
        "右膝关节骨质增生，关节间隙狭窄",  # 应该返回 bone
        "右股骨颈骨折，断端移位",  # 应该返回 fracture
        "双肺纹理增粗，右下肺结节",  # 应该返回 pulmonary
        "腰椎退行性变，椎间盘突出",  # 应该返回 bone
        "左侧肋骨骨折，骨皮质中断",  # 应该返回 fracture
        "右肺下叶炎症，渗出影",  # 应该返回 pulmonary
        "DR检查",  # 应该返回 bone（无明确指示）
    ]
    
    print("测试用例结果:")
    print("=" * 60)
    for case in test_cases:
        prompt_type, body_type = determine_disease_type(case)
        print(f"诊断: {case}")
        print(f"  => {prompt_type} ({body_type})")
        print()
