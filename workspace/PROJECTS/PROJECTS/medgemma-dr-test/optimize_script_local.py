#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地修改测试脚本，添加新的 Prompt
"""
import re

def main():
    print("=" * 70)
    print("本地修改 MedGemma 测试脚本 - 添加新 Prompt")
    print("=" * 70)
    
    orig_path = r'/e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases_backup.py'
    out_path = r'/e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py'
    
    print(f"\n读取脚本: {orig_path}")
    
    try:
        with open(orig_path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return
    
    # 添加 Prompt 常量定义
    prompt_constants = '''
# 骨折识别专用Prompt V7.4
FRACTURE_PROMPT_V74 = """# 骨折识别专用Prompt V7.4

1. 骨皮质连续性检查
   - 必须逐段检查骨皮质是否连续
   - 寻找骨皮质断裂、不连续、移位
   - 关注小骨骼的细微骨折线

2. 高风险漏诊骨折提醒
   - 隐匿性骨折（骨皮质完整但骨小肠紊乱）
   - 应力性骨折（骨皮质外伤但骨小肠断裂）
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
    
    # 插入 Marker
    insert_marker = "# ==================== 扩展映射规则 V7.4 ===================="
    if insert_marker in code:
        code = code.replace(insert_marker, prompt_constants + "\n" + insert_marker)
        print("✅ 已插入 Prompt 常量")
    else:
        print("⚠️ 未找到插入Marker")
    
    # 修改 get_prompt 函数签名
    old_signature = "def get_prompt(body_part):"
    new_signature = "def get_prompt(body_part, use_v74=True):"
    code = code.replace(old_signature, new_signature)
    print("✅ 已修改函数签名为 use_v74=True")
    
    # 修改 prompt 选择逻辑
    old_line = "    body_lower = body_part.lower()\n    if any(kw in body_lower for kw in ["
    
    new_lines = '''    body_lower = body_part.lower()
    if use_v74:
        # 骨折关键词
        if any(kw in body_lower for kw in ['骨折', '断裂', '骨皮质']):
            return FRACTURE_PROMPT_V74, 'fracture'
        # 肺部关键词
        if any(kw in body_lower for kw in ['肺', '胸', '支气管', '肺炎']):
            return PULMONARY_PROMPT_V74, 'pulmonary'
    if any(kw in body_lower for kw in ['''
    
    code = code.replace(old_line, new_lines)
    print("✅ 已修改 prompt 选择逻辑")
    
    # 写入新脚本
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f"✅ 脚本已保存: {out_path}")
    except Exception as e:
        print(f"❌ 保存失败: {e}")
        return
    
    # 统计
    fracture_count = code.count('FRACTURE_PROMPT_V74')
    pulmonary_count = code.count('PULMONARY_PROMPT_V74')
    
    print(f"\n统计结果:")
    print(f"  - FRACTURE_PROMPT_V74: {fracture_count} 个")
    print(f"  - PULMONARY_PROMPT_V74: {pulmonary_count} 个")
    
    print("\n" + "=" * 70)
    print("✅ 优化完成！")
    print("=" * 70)

if __name__ == '__main__':
    main()
