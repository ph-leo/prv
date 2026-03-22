"""
MedGemma V7.4 300病例测试脚本（增强版）

新增功能：
1. 骨折检测增强 Prompt
2. 肺部病变检测增强 Prompt
3. 通用增强 Prompt
4. 支持多视角检查提醒
5. 低识别率病灶专项提示

使用方法：
    python full_test_v7.4_300cases_opt.py [--dataset path] [--output path] [--no-optimization]

版本记录：
- v7.4_opt (2026-03-18): 增强版 Prompt，优化识别率
- v7.4 (2026-03-17): 初始版本
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# ==================== 配置 ====================

MODEL_PATH = r"E:\MedGemma\checkpoints\medgemma-1.5-4b-it"
DEFAULT_DATASET_PATH = r"E:\MedGemma\test_images"
DEFAULT_OUTPUT_PATH = r"E:\MedGemma\outputs\test_v7.4_opt"
DEFAULT_DEVICE = "cuda"  # or "cpu"

# 测试病例分类
TEST_CASES = {
    "fracture": [
        "wrist fracture (scaphoid)",
        "ankle fracture",
        "femoral neck fracture",
        "Colles fracture",
        "tibial plateau fracture",
    ],
    "pulmonary": [
        "pneumothorax",
        "pleural effusion",
        "pneumonia",
        "atelectasis",
        "pulmonary embolism",
    ],
    "generic": [
        "lung nodule",
        "mediastinal mass",
        "spinal fracture",
        "abdominal mass",
    ]
}

# ==================== Prompt 模块 ====================

def get_fracture_prompt(body_part: str = "upper_limb") -> str:
    """获取骨折检测增强版 Prompt"""
    
    return f"""你是一名专业的放射科医生，正在分析骨骼X光或CT影像。

## 骨折诊断核心原则

1. **骨皮质连续性检查（必须逐段检查）**：
   - 仔细检查骨皮质是否连续、平滑
   - 寻找骨皮质中断、扭曲、不规则等异常征象
   - 注意骨皮质边缘是否清晰、整齐

2. **高风险漏诊骨折类型（必须重点检查）**：
   - 隐匿性骨折（Occult Fracture）
   - 应力性骨折（Stress Fracture）
   - 嵌插性骨折（Impaction Fracture）
   - 青枝骨折（Greenstick Fracture）
   - 骨骺分离（Epiphyseal Separation）

3. **{body_part}详细检查清单**：

### 上肢检查（Upper Limb）：
- 肩关节：肩胛骨、锁骨、肱骨头、肱骨外科颈
- 上臂：肱骨骨干、肱骨远端（踝部）
- 前臂：桡骨、尺骨骨干及远端（Colles骨折、Smith骨折）
- 手部：腕骨（舟骨最易漏诊）、掌骨、指骨

### 下肢检查（Lower Limb）：
- 骨盆：髂骨、坐骨、耻骨、髋臼
- 大腿：股骨骨干、股骨颈（老年人高发）
- 膝关节：股骨远端、胫骨平台、髌骨
- 小腿：胫骨、腓骨骨干
- 足部：跗骨（距骨、跟骨）、跖骨、趾骨

### 脊柱检查（Spine）：
- 颈椎：椎体、椎弓、棘突、椎间孔
- 胸椎：椎体、椎弓、肋骨小头
- 腰椎：椎体、椎弓、椎板、横突
- 骶尾骨：骶骨裂孔、尾骨尖

4. **影像征象分析（必须描述）**：
- 直接征象：骨折线、骨皮质中断、骨小梁紊乱
- 间接征象：软组织肿胀、关节积液、骨端移位
- 并发症征象：骨萎缩、骨不连、畸形愈合

5. **报告格式（强制遵守）**：

【骨折诊断报告】

部位定位：[具体部位]

影像学表现：
- 骨皮质连续性：[完整/中断/不规则]
- 骨折线特征：[清晰/模糊/多发]
- 移位情况：[无移位/轻度移位/明显移位/严重移位]
- 成角畸形：[无/有（角度）]
- 旋转畸形：[无/有]
- 临近关节：[受累/未受累]

骨折类型：[明确类型]

鉴别诊断：
- [列出3-5个鉴别诊断]

诊断建议：
- [明确诊断或建议进一步检查]
- "建议CT检查以明确骨折细节"
- "建议MRI检查排除隐匿性骨折"

风险提示：
- [高风险漏诊提醒]
- "舟骨骨折易漏诊，建议短期随访"
- "股骨颈骨折易导致股骨头坏死"

## 特别提醒

⚠️ **高风险漏诊骨折类型必须重点标注**：
- 舟骨骨折（X光早期阴性率高达25%）
- 距骨骨折（血供脆弱，易坏死）
- 股骨颈骨折（老年患者高发，易误诊为扭伤）
- 应力性骨折（早期X光可正常）
- 嵌插性骨折（骨皮质可能保持完整）

请基于影像学特征，严格遵循以上框架进行诊断分析。
"""


def get_pulmonary_prompt() -> str:
    """获取肺部病变检测增强版 Prompt"""
    
    return """你是一名专业的放射科医生，正在分析胸部X光或CT影像。

## 肺部病变分类与特征分析

### 1. 胸膜病变

#### 气胸（Pneumothorax）
**特征描述**：
- 密度：哪里密度减低（负影）
- 边缘：清晰锐利的肺组织边缘
- 分布：肺野外带、肺尖最常见
- 其他：肺门处可见 issuer pattern，纵隔可向对侧移位

**高风险漏诊提醒**：
- 张力性气胸（紧急情况）
- 闭合性气胸（症状轻微易漏诊）
- 医源性气胸（近期插管/穿刺史）

#### 胸腔积液（Pleural Effusion）
**特征描述**：
- 密度：均匀致密影，上缘呈外高内低弧线
- 边缘：清晰，占据肋膈角
- 分布：胸腔下部，大量时可压迫肺组织
- 其他：纵隔向对侧移位，患侧肋间隙增宽

**高风险漏诊提醒**：
- 少量积液（肋膈角变钝即应警惕）
- 包裹性积液（需侧位片或CT确认）
- 血胸（外伤史，密度较高）

### 2. 肺实质病变

#### 肺炎（Pneumonia）
**特征描述**：
- 密度：片状、斑片状实变影
- 边缘：模糊或清晰，可有空气支气管征
- 分布：好发于下肺野、靠近心脏后缘
- 其他：肺纹理增粗，可有空洞、液气平面

#### 肺不张（Atelectasis）
**特征描述**：
- 密度：均匀致密影
- 边缘：清晰，肺门影上移
- 分布：肺叶或肺段分布，体积缩小
- 其他：横膈抬高，纵隔向患侧移位

**高风险漏诊提醒**：
- 代偿性肺气肿（易被误认为正常）
- 小量肺不张（需对比 older 影像）

#### 肺气肿（Emphysema）
**特征描述**：
- 密度：弥漫性低密度区，肺纹理稀疏
- 边缘：肺大疱边界清晰
- 分布：双肺弥漫性，上肺明显
- 其他：横膈低平，心影狭长

### 3. 其他重要病变

#### 肺结核（Tuberculosis）
**高风险漏诊提醒**：
- 浸润性肺结核（与肺炎鉴别）
- 结核球（需与肿瘤鉴别）
- 干酪性肺炎（进展迅速）

#### 肺癌（Lung Cancer）
**高风险漏诊提醒**：
- 周围型肺癌（与良性结节鉴别）
- 小结节（≤1cm，需短期随访）
- 隐匿性肺癌（纵隔淋巴结转移为首发表现）

#### 肺栓塞（Pulmonary Embolism）
**高风险漏诊提醒**：
- 周围型肺梗死（楔形致密影）
- 肺动脉高压（慢性肺栓塞表现）

## 影像征象描述标准（必须包含）

### 密度特征：
- [较低密度 / 正常密度 / 较高密度]
- [均匀 / 不均匀]

### 边缘特征：
- [清晰 / 模糊]
- [规则 / 不规则]
- [分叶状 / 毛刺状 / 脊状突起]

### 分布特征：
- [单侧 / 双侧]
- [局灶性 / 多发性 / 弥漫性]
- [肺野外带 / 肺门周围 / 纵隔旁]
- [上肺 / 中肺 / 下肺]

### 其他特征：
- [伴随征象：空洞、液气平面、钙化等]
- [邻近结构改变：纵隔移位、横膈抬高、胸膜增厚]

## 报告格式（强制遵守）

【胸部影像诊断报告】

影像学表现：
- 病变部位：[具体肺叶/肺段]
- 病变性质：[气胸/积液/肺炎/肺不张/肺气肿]
- 密度特征：[描述]
- 边缘特征：[描述]
- 分布特征：[描述]
- 伴随征象：[描述]

诊断意见：
1. [主要诊断] - [可能性百分比]%
2. [鉴别诊断1]
3. [鉴别诊断2]

建议：
- [建议进一步检查，如CT]
- [建议短期随访]
- [建议临床_correlation]

## 特别提醒

⚠️ **高风险漏诊病变必须重点标注**：
- 气胸：张力性气胸需立即处理
- 积液：少量积液易被忽略
- 肺不张：代偿性肺气肿易被误认为正常
- 肺癌：小结节需短期随访
- 肺栓塞：临床表现不典型时易漏诊
- 肺结核：与肺炎鉴别困难，需结合临床

请基于影像学特征，严格遵循以上框架进行诊断分析。
"""


def get_generic_prompt() -> str:
    """获取通用增强版 Prompt"""
    
    return """你是一名专业的放射科医生，正在分析医学影像（X光、CT、MRI等）。

## 影像诊断核心原则

### 1. 多视角检查提醒（必须考虑）

#### 胸部影像：
- 正位片（PA）：标准检查，评估纵隔、心影、肺门
- 侧位片：定位病变、评估纵隔、心后区
- 侧斜位：评估肺门、支气管
- 高千伏片：观察肺纹理、纵隔结构
- 呼气相：评估肺气肿、气道狭窄
- 吸气相：评估肺实质、膈肌运动

#### CT影像：
- 平扫：评估密度、钙化
- 增强扫描：评估血供、血管侵犯
- 薄层重建（≤1mm）：评估微小病变、骨结构
- MPR重建：多平面评估病变形态
- VR重建：评估骨结构、血管走行

#### MRI影像：
- T1WI：评估脂肪、出血、蛋白含量
- T2WI：评估水肿、液体
- 脂肪抑制：评估出血、水肿
- 增强扫描：评估血供、血脑屏障破坏

### 2. 低识别率病灶专门提示

以下病灶易被漏诊，需特别仔细检查：

**高风险漏诊病灶**：
1. 微小结节（≤5mm）：建议短期随访（3个月）
2. 磨玻璃影（GGO）：建议CT随访（6-12个月）
3. 纵隔淋巴结（≤10mm）：结合临床、PET-CT
4. 胸膜下病变：薄层CT、增强扫描
5. 心后区病变：侧位片、CT扫描
6. 膈顶病变：呼气相、CT扫描
7. 骨皮质内微小病变：骨窗、MRI
8. 血管旁微小结节：增强扫描
9. 脊柱旁病变：冠状/矢状重建
10. 肺尖病变：侧位片、CT薄层扫描

### 3. 影像征象描述标准（必须详细描述）

#### 密度/信号特征：
- [较低密度 / 正常密度 / 较高密度 / 等密度] (CT)
- [低信号 / 等信号 / 高信号 / 混合信号] (MRI)
- [较低密度 / 等密度 / 较高密度 / 气体密度] (X光)
- [均匀 / 不均匀 / 斑片状 / 结节状]

#### 边缘特征：
- [清晰 / 模糊]
- [规则 / 不规则]
- [分叶状 / 毛刺状 / 脊状突起 / 星芒状]
- [光滑 / 粗糙]

#### 分布特征：
- [单侧 / 双侧]
- [局灶性 / 多发性 / 弥漫性]
- [肺野外带 / 肺门周围 / 纵隔旁]
- [上肺 / 中肺 / 下肺]（胸部）

### 4. 报告格式（强制遵守）

【影像诊断报告】

影像学表现：
- 病变部位：[具体解剖位置]
- 病变性质：[可疑/明确诊断]
- 密度/信号：[详细描述]
- 边缘特征：[详细描述]
- 分布特征：[详细描述]
- 大小测量：[长径×短径×层数]
- 数量：[单发/多发/弥漫]
- 形态：[类圆形/不规则/分叶]
- 内部结构：[实性/囊性/混合/钙化]
- 邻近结构：[受累/未受累]
- 远处转移：[有/无]

诊断意见：
1. [最可能诊断] - [可能性百分比]%
2. [第一鉴别诊断]
3. [第二鉴别诊断]
4. [第三鉴别诊断]

建议：
- [建议进一步检查]
- [建议短期随访]
- [建议临床_correlation]
- [建议多学科会诊]

## 特别提醒

⚠️ **低识别率病灶必须重点标注**：
- 微小结节（≤5mm）：建议短期随访
- 磨玻璃影（GGO）：建议CT随访
- 纵隔淋巴结（≤10mm）：结合临床
- 胸膜下病变：薄层CT、增强扫描
- 心后区病变：侧位片、CT
- 膈顶病变：呼气相、CT
- 骨皮质内病变：骨窗、MRI
- 血管旁病变：增强扫描
- 脊柱旁病变：冠状/矢状重建
- 肺尖病变：侧位片、CT薄层

请基于影像学特征，严格遵循以上框架进行诊断分析。
"""


def get_prompt(body_part: str = "chest", use_v74_opt: bool = False) -> str:
    """
    获取 Prompt（支持新旧版本）
    
    参数:
        body_part: 体部部位 (chest/abdomen/brain/upper_limb/lower_limb/spine)
        use_v74_opt: 是否使用 V7.4 增强版 Prompt
    
    返回:
        Prompt 字符串
    """
    
    if not use_v74_opt:
        # 旧版 Prompt
        return f"请分析这组影像，重点关注 {body_part} 区域的异常表现。"
    
    # V7.4 增强版 Prompt
    body_part_lower = body_part.lower()
    
    if body_part_lower in ["upper_limb", "arm", "hand", "wrist", "shoulder", "elbow"]:
        return get_fracture_prompt("upper_limb")
    
    elif body_part_lower in ["lower_limb", "leg", "foot", "hip", "knee", "ankle"]:
        return get_fracture_prompt("lower_limb")
    
    elif body_part_lower in ["spine", "spinal", "back", "neck"]:
        return get_fracture_prompt("spine")
    
    elif body_part_lower in ["chest", "lung", "pulmonary", "thoracic"]:
        return get_pulmonary_prompt()
    
    else:
        # 默认通用 Prompt
        return get_generic_prompt()


# ==================== 测试执行器 ====================

class MedGemmaTester:
    """MedGemma 测试执行器（增强版）"""
    
    def __init__(self, model_path: str = MODEL_PATH, device: str = DEFAULT_DEVICE):
        self.model_path = model_path
        self.device = device
        self.model = None
        self.processor = None
        self.results = []
        self.start_time = None
    
    def load_model(self):
        """加载模型"""
        print(f"正在加载模型: {self.model_path}")
        
        from transformers import AutoProcessor, AutoModelForImageTextToText
        import torch
        
        self.processor = AutoProcessor.from_pretrained(self.model_path)
        
        self.model = AutoModelForImageTextToText.from_pretrained(
            self.model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )
        
        print(f"模型加载完成，设备: {self.model.device}")
    
    def analyze_image(
        self, 
        image_path: str, 
        prompt: str,
        window_type: str = "original"
    ) -> Tuple[str, float]:
        """
        分析单张影像
        
        返回:
            (诊断结果, 耗时)
        """
        from PIL import Image
        import pydicom
        import numpy as np
        import torch
        
        start_time = datetime.now()
        
        # 加载影像
        if image_path.lower().endswith('.dcm'):
            ds = pydicom.dcmread(image_path)
            slope = getattr(ds, 'RescaleSlope', 1)
            intercept = getattr(ds, 'RescaleIntercept', 0)
            image = ds.pixel_array * slope + intercept
            
            # 应用窗宽窗位
            presets = {
                "lung": (-600, 1500),
                "mediastinal": (50, 350),
                "bone": (400, 1000),
                "brain": (40, 80),
                "abdomen": (40, 400),
            }
            
            if window_type in presets:
                center, width = presets[window_type]
                image = np.clip(image, center - width // 2, center + width // 2)
            
            image = ((image - image.min()) / (image.max() - image.min()) * 255).astype(np.uint8)
            pil_image = Image.fromarray(image).convert('RGB')
        else:
            pil_image = Image.open(image_path).convert('RGB')
        
        # 构建消息
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": pil_image},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
        
        # 应用 chat template
        inputs = self.processor.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device, dtype=torch.bfloat16)
        
        input_len = inputs["input_ids"].shape[-1]
        
        # 生成
        with torch.inference_mode():
            generation = self.model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=False
            )
        
        generation = generation[0][input_len:]
        result = self.processor.decode(generation, skip_special_tokens=True)
        
        elapsed_time = (datetime.now() - start_time).total_seconds()
        
        return result, elapsed_time
    
    def run_test(
        self, 
        dataset_path: str,
        output_path: str,
        use_v74_opt: bool = True,
        max_cases: int = 300
    ):
        """
        运行测试
        
        参数:
            dataset_path: 数据集路径
            output_path: 输出路径
            use_v74_opt: 是否使用 V7.4 增强版 Prompt
            max_cases: 最大测试病例数
        """
        self.start_time = datetime.now()
        
        print(f"\n{'='*60}")
        print("MedGemma V7.4 测试 (增强版)")
        print(f"{'='*60}")
        print(f"数据集路径: {dataset_path}")
        print(f"输出路径: {output_path}")
        print(f"使用增强版 Prompt: {use_v74_opt}")
        print(f"最大测试病例数: {max_cases}")
        print(f"{'='*60}\n")
        
        # 创建输出目录
        os.makedirs(output_path, exist_ok=True)
        
        # 收集测试文件
        test_files = []
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file.lower().endswith(('.dcm', '.png', '.jpg', '.jpeg')):
                    test_files.append(os.path.join(root, file))
        
        print(f"发现测试文件: {len(test_files)} 个")
        
        if max_cases > 0:
            test_files = test_files[:max_cases]
        
        # 运行测试
        for i, image_path in enumerate(test_files):
            print(f"\n处理 [{i+1}/{len(test_files)}] {os.path.basename(image_path)} ...")
            
            # 根据文件名推断部位
            filename = os.path.basename(image_path).lower()
            
            if any(x in filename for x in ['wrist', 'hand', 'arm', 'shoulder', 'elbow']):
                body_part = "upper_limb"
            elif any(x in filename for x in ['ankle', 'foot', 'leg', 'hip', 'knee']):
                body_part = "lower_limb"
            elif any(x in filename for x in ['chest', 'lung', 'thoracic']):
                body_part = "chest"
            elif any(x in filename for x in ['spine', 'back', 'neck']):
                body_part = "spine"
            else:
                body_part = "generic"
            
            # 获取 Prompt
            prompt = get_prompt(body_part, use_v74_opt=use_v74_opt)
            
            # 分析影像
            try:
                result, elapsed_time = self.analyze_image(image_path, prompt)
                
                # 保存结果
                result_entry = {
                    "image_path": image_path,
                    "body_part": body_part,
                    "prompt_type": "v7.4_opt" if use_v74_opt else "v7.4",
                    "elapsed_time": elapsed_time,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.results.append(result_entry)
                
                # 输出摘要
                print(f"  ✓ 完成 (${elapsed_time:.2f}s)")
                print(f"  部位: {body_part}")
                
            except Exception as e:
                print(f"  ✗ 错误: {str(e)}")
                error_entry = {
                    "image_path": image_path,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                self.results.append(error_entry)
        
        # 保存完整结果
        self.save_results(output_path)
        
        # 生成测试报告
        self.generate_report(output_path)
    
    def save_results(self, output_path: str):
        """保存测试结果"""
        import json
        
        result_file = os.path.join(output_path, "test_results.json")
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        print(f"\n结果已保存: {result_file}")
    
    def generate_report(self, output_path: str):
        """生成测试报告"""
        import json
        
        # 统计信息
        total_cases = len(self.results)
        successful_cases = sum(1 for r in self.results if 'result' in r)
        failed_cases = total_cases - successful_cases
        elapsed_total = (datetime.now() - self.start_time).total_seconds()
        
        # 平均耗时
        times = [r['elapsed_time'] for r in self.results if 'elapsed_time' in r]
        avg_time = sum(times) / len(times) if times else 0
        
        report = {
            "test_summary": {
                "total_cases": total_cases,
                "successful_cases": successful_cases,
                "failed_cases": failed_cases,
                "success_rate": successful_cases / total_cases * 100 if total_cases > 0 else 0,
                "total_time_seconds": elapsed_total,
                "avg_time_per_case": avg_time,
                "timestamp": self.start_time.isoformat(),
                "end_timestamp": datetime.now().isoformat()
            },
            "prompt_optimization": "v7.4_opt" if any(r.get('prompt_type') == 'v7.4_opt' for r in self.results) else "v7.4",
            "results": self.results
        }
        
        report_file = os.path.join(output_path, "test_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 打印摘要
        print(f"\n{'='*60}")
        print("测试完成摘要")
        print(f"{'='*60}")
        print(f"总病例数: {total_cases}")
        print(f"成功病例: {successful_cases}")
        print(f"失败病例: {failed_cases}")
        print(f"成功率: {report['test_summary']['success_rate']:.1f}%")
        print(f"总耗时: {elapsed_total:.2f} 秒")
        print(f"平均耗时: {avg_time:.2f} 秒/例")
        print(f"{'='*60}")
        
        print(f"\n报告已保存: {report_file}")


# ==================== 主程序 ====================

def main():
    parser = argparse.ArgumentParser(description="MedGemma V7.4 300病例测试脚本（增强版）")
    parser.add_argument("--dataset", type=str, default=DEFAULT_DATASET_PATH,
                        help=f"数据集路径 (default: {DEFAULT_DATASET_PATH})")
    parser.add_argument("--output", type=str, default=DEFAULT_OUTPUT_PATH,
                        help=f"输出路径 (default: {DEFAULT_OUTPUT_PATH})")
    parser.add_argument("--no-optimization", action="store_true",
                        help="使用旧版 Prompt（不使用增强版）")
    parser.add_argument("--max-cases", type=int, default=300,
                        help="最大测试病例数 (default: 300)")
    parser.add_argument("--device", type=str, default=DEFAULT_DEVICE,
                        help="设备类型 (cuda/cpu, default: cuda)")
    
    args = parser.parse_args()
    
    # 创建测试器
    tester = MedGemmaTester(device=args.device)
    
    # 加载模型
    tester.load_model()
    
    # 运行测试
    tester.run_test(
        dataset_path=args.dataset,
        output_path=args.output,
        use_v74_opt=not args.no_optimization,
        max_cases=args.max_cases
    )


if __name__ == "__main__":
    main()
