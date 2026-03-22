# -*- coding: utf-8 -*-
"""
验证 Prompt 选择逻辑
"""

def get_prompt_test(body_part, use_v74=True):
    body_lower = body_part.lower()
    if use_v74:
        # 骨折关键词
        if any(kw in body_lower for kw in ['骨折', '断裂', '骨皮质']):
            return 'fracture', 'FRACTURE_PROMPT_V74'
        # 肺部关键词
        if any(kw in body_lower for kw in ['肺', '胸', '支气管', '肺炎']):
            return 'pulmonary', 'PULMONARY_PROMPT_V74'
        # 骨骼关键词（脊柱/关节）
        if any(kw in body_lower for kw in ['脊柱', '颈椎', '胸椎', '腰椎', '关节', '骨', '上肢', '下肢', '肢体']):
            return 'bone', 'SKELETAL_PROMPT_V74'
        # 骨折关键词（扩展）
        if '骨折' in body_lower:
            return 'fracture', 'FRACTURE_PROMPT_V74'
    # fallback
    if any(kw in body_lower for kw in ['胸', 'chest', '肺', '心']):
        return 'chest', 'CHEST_PROMPT_V72'
    elif any(kw in body_lower for kw in ['上肢', '下肢', '骨', '肢体', '手', '足', '关节', '脊柱']):
        return 'bone', 'SKELETAL_PROMPT_V74'
    return 'generic', 'GENERIC_PROMPT_V72'

# 测试用例
test_cases = [
    ("右手骨折", "fracture"),
    ("胸部CT", "pulmonary"),
    ("左腿骨折", "fracture"),
    ("肺部炎症", "pulmonary"),
    ("颈椎检查", "bone"),
    ("胸廓对称", "pulmonary"),
    ("腰椎检查", "bone"),
    ("膝关节", "bone"),
    ("上肢", "bone"),
    ("下肢", "bone"),
]

print("Prompt 选择逻辑测试结果:")
print("=" * 60)
passed = 0
failed = 0
for body_part, expected in test_cases:
    prompt_type, prompt_name = get_prompt_test(body_part)
    status = 'OK' if prompt_type == expected else 'FAIL'
    if status == 'OK':
        passed += 1
    else:
        failed += 1
    print(f"{status} {body_part:15} -> {prompt_type:12} (期望: {expected:12})")
print("=" * 60)
print(f"通过: {passed}, 失败: {failed}")
