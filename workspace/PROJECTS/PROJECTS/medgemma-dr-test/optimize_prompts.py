# MedGemma V7.4 识别率优化 - 批量替换Prompts
# 使用方法:
# 1. 在开发电脑下载此脚本
# 2. 运行: python optimize_prompts.py
# 3. 运行测试: python full_test_v7.4_300cases.py
# 4. 对比识别率提升情况

import re
from pathlib import Path

# 原始脚本路径
ORIGINAL_SCRIPT = Path(r"E:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases_backup.py")
# 输出脚本路径
OUTPUT_SCRIPT = Path(r"E:\ai_test_MedGemma\ai\other\scripts\full_test_v7.4_300cases.py")

def optimize_script():
    """优化测试脚本"""
    print("=" * 70)
    print("MedGemma V7.4 识别率优化 - Prompt替换工具")
    print("=" * 70)
    
    # 读取原始脚本
    if not ORIGINAL_SCRIPT.exists():
        print(f"\n错误: 原始脚本不存在: {ORIGINAL_SCRIPT}")
        return False
    
    print(f"\n✓ 读取原始脚本: {ORIGINAL_SCRIPT}")
    print(f"  大小: {ORIGINAL_SCRIPT.stat().st_size} 字节")
    
    with open(ORIGINAL_SCRIPT, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经优化
    if 'FRACTURE_PROMPT_V74' in content:
        print("\n✅ 脚本已被优化，跳过替换")
        return True
    
    # 替换Prompt
    print("\n执行优化:")
    
    # 1. 替换骨皮质检查关键词
    content = content.replace(
        "Look carefully at small bones (phalanges, carpal/tarsal bones) for subtle fracture lines.",
        """# Step 1: 骨皮质检查（关键）
        1. 仔细检查每块骨骼的骨皮质是否连续
        2. 寻找骨皮质断裂、不连续、移位
        3. 特别关注小骨骼（指骨、趾骨、小腕骨）的细微骨折线"""
    )
    
    # 2. 替换肺部检查关键词
    content = content.replace(
        "IMPORTANT: Report aortic calcification and vascular calcification as positive findings.",
        """#肺部病变识别专用Prompt (CHEST X-RAY)
        # Step 1: 整体评估
        1. 肺野是否清晰
        2. 肺纹理是否增粗、紊乱
        3. 肺门是否增大、模糊
        4. 膈肌是否抬高、变平
        5. 纵隔是否移位"""
    )
    
    # 3. 添加骨折专用Prompt
    fracture_keywords = ['骨折', '断裂', '骨皮质', '粉碎', '嵌插']
    content = content.replace(
        "# ==================== 扩展映射规则 V7.4 ====================",
        """# ==================== 优化后的骨折专用Prompt V7.4 ====================
通过强化骨皮质检查和骨折检查清单，提升骨折识别率

# ==================== 优化后的肺部专用Prompt V7.4 ====================
通过细化肺部病变分类，提升肺部病变识别率

# ==================== 扩展映射规则 V7.4 ===================="""
    )
    
    # 保存优化后的脚本
    OUTPUT_SCRIPT.write_text(content, encoding='utf-8')
    
    print(f"\n✓ 保存优化后的脚本: {OUTPUT_SCRIPT}")
    print(f"  大小: {OUTPUT_SCRIPT.stat().st_size} 字节")
    
    # 验证优化
    with open(OUTPUT_SCRIPT, 'r', encoding='utf-8') as f:
        new_content = f.read()
    
    print("\n优化验证:")
    checks = [
        ('单骨皮质检查增强', '骨皮质连续' in new_content),
        ('骨折检查清单', '锁骨' in new_content and '肱骨' in new_content),
        ('高风险提醒', '隐匿性骨折' in new_content),
        ('肺部病变分类', '肺叶' in new_content and '肺段' in new_content),
    ]
    
    all_passed = True
    for name, passed in checks:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n" + "=" * 70)
        print("✅ 优化完成！")
        print("=" * 70)
        print("\n下一步:")
        print("1. 运行测试: python full_test_v7.4_300cases.py")
        print("2. 对比识别率提升情况")
        return True
    else:
        print("\n❌ 部分优化未生效，请检查")
        return False

if __name__ == '__main__':
    success = optimize_script()
    input("\n按回车键退出...")
