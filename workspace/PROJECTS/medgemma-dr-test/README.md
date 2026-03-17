# MedGemma DR 测试项目文档

**项目版本**: v1.0  
**最后更新**: 2026-03-17  
**适用对象**: 测试工程师  

---

## 📚 项目导航

如果文档丢失，请记住以下关键词快速查找：
- **项目关键词**: `MedGemma DR 测试`、`ai_test_MedGemma`
- **关键字**: `测试工程师职责`、`测试执行指南`、`开发电脑连接`
- **路径定位**: 查找 `ai_test_MedGemma` 目录即可找到项目

---

## 🎯 测试目标

| 项目 | 说明 |
|------|------|
| **测试模型** | MedGemma 1.5 4B (IT 版本) |
| **测试数据** | 300 个 DICOM 病例（DR 胸部/骨骼影像） |
| **AI 服务** | http://localhost:8000/analyze_batch |
| **测试脚本** | `scripts/full_test_v7.4_300cases.py` |
| **预计时长** | 30-40 分钟 |

---

## 🔌 开发电脑连接信息（固定配置）

### 💻 远程连接方式

```bash
# SSH 连接命令（固定，不要修改）
ssh -p 12222 D@127.0.0.1

# 验证连接
ssh -p 12222 D@127.0.0.1 "hostname && whoami"
```

### 📂 固定路径配置（全部在开发电脑上）

```bash
# 连接开发电脑后，所有路径都是相对于此环境
# 以下路径是固定的，不需要任何询问

# 项目根目录
BASE_DIR="/e/ai_test_MedGemma/ai/other"

# 测试数据目录（DICOM 原始数据）
# ⚠️ 这些是原始数据，禁止复制、上传、转移！
TESTFILE_DIR="/e/ai_test_MedGemma/ai/other/testfile300-20260312/test_study300"

# 图像转换目录（CLAHE 预处理后）
CONVERTED_DIR="/e/ai_test_MedGemma/ai/other/converted_images_v74"

# 测试结果输出目录
OUTPUT_DIR="/e/ai_test_MedGemma/ai/other/test_results/v7.4_300cases"

# 输入 Excel 文件
INPUT_EXCEL="/e/ai_test_MedGemma/ai/other/testfile300-20260312/测试记录20260312-300.xlsx"

# 测试脚本位置
TEST_SCRIPT="/e/ai_test_MedGemma/ai/other/scripts/full_test_v7.4_300cases.py"
```

### 🔍 验证路径是否正确

```bash
# 连接开发电脑后执行以下命令验证
ssh -p 12222 D@127.0.0.1 "
cd /e/ai_test_MedGemma/ai/other &&
ls -la &&
echo '=== 数据目录 ===' &&
ls testfile300-20260312/test_study300 | head -5 &&
echo '=== 脚本位置 ===' &&
ls scripts/full_test_v7.4_300cases.py
"
```

---

## 🛡️ 测试工程师职责（强制执行）

### 🚫 **绝对禁止行为（安全红线）**

| 行为 | 禁止级别 | 说明 |
|------|---------|------|
| ❌ 复制任何文件到本地 | 🔴 高危 | 包括 DICOM 原始数据、测试结果 |
| ❌ 上传文件到任何服务器 | 🔴 高危 | 包括 HuggingFace、GitHub、公司服务器 |
| ❌ 发送文件到外部邮箱 | 🔴 高危 | 任何文件都不允许外发 |
| ❌ 拷贝到外部存储设备 | 🔴 高危 | U盘、移动硬盘等全部禁止 |
| ❌ 截图发送给他人 | 🟡 中危 | 包括测试结果、Excel、Markdown 报告 |

### ✅ **必须遵守行为**

| 行为 | 要求 | 说明 |
|------|------|------|
| ✅ 所有测试数据留存在开发电脑 | 🔒 强制 | DICOM、转换图像、测试结果都在开发电脑 |
| ✅ 测试结果仅保存在本地路径 | 🔒 强制 | 只能保存在 `/e/ai_test_MedGemma/ai/other` |
| ✅ 生成的文件命名包含时间戳 | 🔒 强制 | 避免覆盖之前的测试结果 |
| ✅ 测试前后检查磁盘空间 | 🔒 强制 | 确保有足够空间存储转换图像和结果 |

### 📋 **测试执行流程（固定步骤）**

```bash
# 1. SSH 连接开发电脑（固定方式）
ssh -p 12222 D@127.0.0.1

# 2. 导航到项目目录（固定路径）
cd /e/ai_test_MedGemma/ai/other

# 3. 检查 AI 服务状态
curl http://localhost:8000/health

# 4. 执行测试脚本
python scripts/full_test_v7.4_300cases.py

# 5. 查看测试结果
ls test_results/v7.4_300cases/
ls /e/ai_test_MedGemma/ai/other/测试记录_*.xlsx
```

---

## 🧪 测试执行指南

### 📋 **测试前检查清单**

```bash
# SSH 连接开发电脑后，逐项检查

# 1. Python 环境
python --version  # 需要 Python 3.8+

# 2. 依赖包安装检查
pip list | grep -E "pydicom|numpy|pillow|opencv-python|openpyxl|requests"

# 3. GPU 可用性
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"

# 4. AI 服务状态（关键！必须响应）
curl http://localhost:8000/health
# 预期输出: {"status":"healthy","model_loaded":true,"device":"cuda:0"}

# 5. Excel 输入文件存在
ls /e/ai_test_MedGemma/ai/other/testfile300-20260312/测试记录20260312-300.xlsx

# 6. DICOM 数据目录
ls /e/ai_test_MedGemma/ai/other/testfile300-20260312/test_study300 | wc -l
# 应该显示约 300 个文件夹
```

### ▶️ **执行测试**

```bash
# SSH 连接开发电脑后执行
cd /e/ai_test_MedGemma/ai/other

# 执行测试（约 30-40 分钟）
python scripts/full_test_v7.4_300cases.py

# 测试过程中会自动：
# 1. 读取 Excel 中的 300 个病例
# 2. 将 DICOM 转换为 PNG（CLAHE 增强）
# 3. 调用 AI API 进行分析
# 4. 与专家诊断对比计算准确率
# 5. 生成 Markdown 报告和 Excel 结果
```

### 📊 **查看测试结果**

```bash
# 生成的文件会保存在以下位置（固定路径）

# Markdown 报告（汇总报告）
ls /e/ai_test_MedGemma/ai/other/test_results/v7.4_300cases/summary_report_*.md

# Excel 结果（详细数据）
ls /e/ai_test_MedGemma/ai/other/测试记录_V7.2_300cases_*.xlsx

# 查看 Markdown 报告内容
cat /e/ai_test_MedGemma/ai/other/test_results/v7.4_300cases/summary_report_*.md
```

---

## 📁 测试结果文件格式

### 📄 Markdown 报告 (`summary_report_V7.4_300cases_*.md`)

包含以下内容：
- **总体统计**: 总病例数、成功/失败数、整体准确率
- **各病种统计表**: 每种病灶的识别率（肺炎、骨折、积液等）
- **详细结果**: 300 个病例的每一条测试数据

### 📊 Excel 结果 (`测试记录_V7.2_300cases_*.xlsx`)

包含以下列：
| 列名 | 说明 |
|------|------|
| 病例ID | DICOM 文件夹名 |
| 部位 | 胸部/脊柱/四肢等 |
| 医生诊断 | Excel 中的原始诊断 |
| AI检出 | AI 正确识别的病灶 |
| AI漏检 | AI 未识别的病灶 |
| 准确率% | 单个病例的识别准确率 |
| 推理时间 | AI 响应耗时 |
| AI分析摘要 | AI 生成的完整报告 |

---

## 🐛 常见问题处理

### ❌ AI 服务无响应

```bash
# 检查服务是否运行
netstat -tlnp | grep 8000

# 启动 AI 服务（在另一个终端）
cd /e/ai_test_MedGemma/scripts
python medgemma_api_plus.py
```

### ❌ DICOM 转换失败

```bash
# 检查 DICOM 文件
ls /e/ai_test_MedGemma/ai/other/testfile300-20260312/test_study300/{case_id}

# 手动测试 DICOM 读取
python -c "import pydicom; ds = pydicom.dcmread('{case_dir}'); print(ds.PatientName)"
```

### ❌ 磁盘空间不足

```bash
# 检查磁盘空间
df -h /e

# 清理转换图像（如果需要）
rm -rf /e/ai_test_MedGemma/ai/other/converted_images_v74/*
```

---

## 📞 问题排查流程

### 当测试遇到问题时：

1. **记录错误信息**（不要自行修改脚本）
2. **检查以上"常见问题处理"章节**
3. **如果无法解决，等待远程协助**

### 需要提供的信息：

```
1. 错误时间：_________
2. 错误命令：_________
3. 完整错误信息：_________
4. 已尝试的解决方法：_________
```

---

## ✅ 测试完成检查

执行测试后，必须确认以下文件生成：

```bash
# 列出所有生成的文件
ls -la /e/ai_test_MedGemma/ai/other/测试记录_V7.2_*.xlsx
ls -la /e/ai_test_MedGemma/ai/other/test_results/v7.4_300cases/summary_report_*.md

# 检查报告内容完整性
head -30 /e/ai_test_MedGemma/ai/other/test_results/v7.4_300cases/summary_report_*.md
```

### 📝 提交测试结果

测试完成后，**只发送以下信息**：

```
1. Markdown 报告文件名：summary_report_V7.4_300cases_*.md
2. Excel 结果文件名：测试记录_V7.2_300cases_*.xlsx
3. 总体准确率：______%
4. 成功/失败病例数：______/______
```

---

## 🔗 项目快速定位

如果文档丢失，请按以下方式找回项目：

### 方法 1：路径搜索（最快）
```bash
# 在开发电脑上寻找包含 'ai_test_MedGemma' 的路径
find /e -name "*ai_test_MedGemma*" -type d 2>/dev/null
# 或
ls /e/ai_test_MedGemma/
```

### 方法 2：关键词搜索
- 搜索 `ai_test_MedGemma`
- 搜索 `medgemma dr 测试`
- 搜索 `测试记录20260312-300.xlsx`

### 方法 3：连接方式记忆
- 连接命令：`ssh -p 12222 D@127.0.0.1`
- 端口固定：12222
- 用户名固定：D
- 主机固定：127.0.0.1（SSH 隧道）

---

## 📌 重要提醒

1. **安全第一**: 所有测试数据都在开发电脑，禁止任何形式的文件外传
2. **路径固定**: 不需要询问任何路径信息，全部已在此文档说明
3. **连接固定**: SSH 连接方式固定，不需要询问
4. **测试标准**: 必须使用 `full_test_v7.4_300cases.py` 脚本
5. **结果保存**: 测试结果只能保存在开发电脑指定路径

---

---

## 📚 文档索引

本项目包含以下文档，请按需查阅：

| 文档 | 说明 |
|------|------|
| **README.md** (本文档) | 完整项目文档，包含测试执行指南 |
| **职责清单.md** | 测试工程师职责、禁止行为清单 |
| **快速定位指南.md** | 项目快速定位方法 |
| **项目结构.md** | 项目完整目录结构 |

---

## 🔑 关键信息速查表（必须记住）

| 类型 | 信息 | 状态 |
|------|------|------|
| **SSH 连接** | `ssh -p 12222 D@127.0.0.1` | 🔒 固定 |
| **项目路径** | `/e/ai_test_MedGemma/ai/other` | 🔒 固定 |
| **测试脚本** | `scripts/full_test_v7.4_300cases.py` | 🔒 固定 |
| **Excel 输入** | `测试记录20260312-300.xlsx` | 🔒 固定 |

---

## 📞 测试准备检查清单

执行测试前，请确认：

- [ ] SSH 连接成功: `ssh -p 12222 D@127.0.0.1`
- [ ] AI 服务正常: `curl http://localhost:8000/health`
- [ ] Excel 文件存在: `ls .../测试记录20260312-300.xlsx`
- [ ] DICOM 数据存在: `ls .../test_study300/ | wc -l`
- [ ] 磁盘空间充足: `df -h /e`

---

**重要提醒**:

---

## 📚 文档索引

本项目包含以下文档，请按需查阅：

| 文档 | 说明 |
|------|------|
| **README.md** (本文档) | 完整项目文档，包含测试执行指南 |
| **职责清单.md** | 测试工程师职责、禁止行为清单 |
| **快速定位指南.md** | 项目快速定位方法 |
| **项目结构.md** | 项目完整目录结构 |
| **方案确认.md** | 测试执行方案确认 |

---

## 🔑 关键信息速查表（必须记住）

| 类型 | 信息 | 状态 |
|------|------|------|
| **SSH 连接** | `ssh -p 12222 D@127.0.0.1` | 🔒 固定 |
| **项目路径** | `/e/ai_test_MedGemma/ai/other` | 🔒 固定 |
| **测试脚本** | `scripts/full_test_v7.4_300cases.py` | 🔒 固定 |
| **Excel 输入** | `测试记录20260312-300.xlsx` | 🔒 固定 |

---

## 📞 测试准备检查清单

执行测试前，请确认：

- [ ] SSH 连接成功: `ssh -p 12222 D@127.0.0.1`
- [ ] AI 服务正常: `curl http://localhost:8000/health`
- [ ] Excel 文件存在: `ls .../测试记录20260312-300.xlsx`
- [ ] DICOM 数据存在: `ls .../test_study300/ | wc -l`
- [ ] 磁盘空间充足: `df -h /e`

---

---

## 🔗 项目快速定位

如果文档丢失，请按以下方式找回项目：

### 方法 1：路径搜索（最快）
```bash
# 在开发电脑上寻找包含 'ai_test_MedGemma' 的路径
find /e -name "*ai_test_MedGemma*" -type d 2>/dev/null
# 或
ls /e/ai_test_MedGemma/
```

### 方法 2：关键词搜索
- 搜索 `ai_test_MedGemma`
- 搜索 `medgemma dr 测试`
- 搜索 `测试记录20260312-300.xlsx`

### 方法 3：连接方式记忆
- 连接命令：`ssh -p 12222 D@127.0.0.1`
- 端口固定：12222
- 用户名固定：D
- 主机固定：127.0.0.1（SSH 隧道）

---

## 🔐 安全红线（强制执行）

| 禁止行为 | 风险级别 |
|----------|----------|
| ❌ 复制任何文件到本地 | 🔴 高危 |
| ❌ 上传文件到服务器 | 🔴 高危 |
| ❌ 发送文件到外部邮箱 | 🔴 高危 |
| ❌ 截图发送给他人 | 🟡 中危 |

---

## 📝 测试完成检查

执行测试后，必须确认以下文件生成：

```bash
# 列出所有生成的文件
ls -la /e/ai_test_MedGemma/ai/other/测试记录_V7.2_*.xlsx
ls -la /e/ai_test_MedGemma/ai/other/test_results/v7.4_300cases/summary_report_*.md

# 检查报告内容完整性
head -30 /e/ai_test_MedGemma/ai/other/test_results/v7.4_300cases/summary_report_*.md
```

### 📤 提交测试结果

测试完成后，**只发送以下信息**：

```
1. Markdown 报告文件名：summary_report_V7.4_300cases_*.md
2. Excel 结果文件名：测试记录_V7.2_300cases_*.xlsx
3. 总体准确率：______%
4. 成功/失败病例数：______/______
```

---

## 📚 文档索引

本项目包含以下文档，请按需查阅：

| 文档 | 说明 |
|------|------|
| **README.md** (本文档) | 完整项目文档，包含测试执行指南 |
| **职责清单.md** | 测试工程师职责、禁止行为清单 |
| **快速定位指南.md** | 项目快速定位方法 |
| **项目结构.md** | 项目完整目录结构 |
| **方案确认.md** | 测试执行方案确认 |

---

## 🔑 关键信息速查表（必须记住）

| 类型 | 信息 | 状态 |
|------|------|------|
| **SSH 连接** | `ssh -p 12222 D@127.0.0.1` | 🔒 固定 |
| **项目路径** | `/e/ai_test_MedGemma/ai/other` | 🔒 固定 |
| **测试脚本** | `scripts/full_test_v7.4_300cases.py` | 🔒 固定 |
| **Excel 输入** | `测试记录20260312-300.xlsx` | 🔒 固定 |

---

## 📞 测试准备检查清单

执行测试前，请确认：

- [ ] SSH 连接成功: `ssh -p 12222 D@127.0.0.1`
- [ ] AI 服务正常: `curl http://localhost:8000/health`
- [ ] Excel 文件存在: `ls .../测试记录20260312-300.xlsx`
- [ ] DICOM 数据存在: `ls .../test_study300/ | wc -l`
- [ ] 磁盘空间充足: `df -h /e`

---

## 📁 文档位置

所有文档都保存在：
```
/root/.openclaw/workspace/PROJECTS/medgemma-dr-test/
```

如果需要分享给测试工程师，可以：
1. **复制整个目录**
2. **发送文档链接**
3. **打印关键页面**（职责清单、快速定位指南）

---

## ✅ 方案确认

请确认以下内容：

- [x] SSH 连接方式已固定（端口 12222，用户 D，主机 127.0.0.1）
- [x] 项目路径已固定（/e/ai_test_MedGemma/ai/other）
- [x] 测试脚本已指定（scripts/full_test_v7.4_300cases.py）
- [x] 测试工程师职责已明确（禁止行为清单）
- [x] 快速定位方法已提供（4种方法）
- [x] 文档位置已保存（/root/.openclaw/workspace/PROJECTS/medgemma-dr-test/）

---

**文档版本**: v1.0  
**更新日期**: 2026-03-17  
**适用版本**: MedGemma V7.4 测试脚本
