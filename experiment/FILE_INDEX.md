# 📑 文件索引

## 快速导航

### 🔴 必读文件

1. **QUICK_START.md** ⭐⭐⭐
   - 快速开始指南
   - 一键启动命令
   - 常见问题解决

2. **PROJECT_DOCUMENTATION.md** ⭐⭐⭐
   - 完整项目文档
   - 技术说明
   - API 参考

3. **COMPLETION_REPORT.md** ⭐⭐
   - 项目完成报告
   - 实验结果统计
   - 交付物清单

---

## 脚本文件

### 核心脚本

| 文件 | 用途 | 推荐度 |
|------|------|--------|
| `process_complete_dataset.py` | 处理完整数据集（164 条）✅ | ⭐⭐⭐ |
| `grammar_constrained_decoding.py` | 处理小数据集（6 条） | ⭐⭐ |
| `compare_results.py` | 对比两个数据集结果 | ⭐⭐ |

### 辅助脚本

| 文件 | 用途 |
|------|------|
| `run_full_experiment.py` | 实验启动器（已集成） |

---

## 配置文件

| 文件 | 内容 |
|------|------|
| `python_grammar.lark` | Python 语法定义（Lark 格式） |

---

## 输出文件

### result_comp/（完整数据集结果）✅ 推荐查看

```
result_comp/
├── json_schema_outlines.json  ⭐ 主要输出
│   └── 164 条 JSON Schema 记录 (0.49 MB)
├── processed_samples.json
│   └── 处理后的代码样本 (0.25 MB)
└── experiment_summary.json
    └── 统计数据 (1 KB)
```

### results/（小数据集结果）参考

```
results/
├── json_schema_outlines.json
│   └── 6 条 JSON Schema 记录
├── processed_samples.json
│   └── 处理后的代码样本
└── experiment_summary.json
    └── 统计数据
```

---

## 文档文件

| 文件 | 描述 | 长度 |
|------|------|------|
| `QUICK_START.md` | 快速开始指南 | 中等 |
| `PROJECT_DOCUMENTATION.md` | 完整文档 | 长 (12 章) |
| `COMPLETION_REPORT.md` | 完成报告 | 长 |
| `FILE_INDEX.md` | 本文件 | 中等 |

---

## 数据文件

### 输入数据

| 路径 | 格式 | 大小 | 记录数 |
|------|------|------|--------|
| `../Data/human-eval-master/data/HumanEval.jsonl.gz` | JSONL.GZ | ~300 KB | 164 |
| `../Data/human-eval-master/data/example_samples.jsonl` | JSONL | ~2 KB | 6 |

---

## 命令速查表

### 1️⃣ 激活虚拟环境

```powershell
# Windows PowerShell
& "d:\新建文件夹\A SCNU\项目\AI教育\TDD\alignment_env\Scripts\Activate.ps1"

# 验证激活
python --version
```

### 2️⃣ 运行脚本

```powershell
cd "d:\新建文件夹\A SCNU\项目\AI教育\TDD\experiment"

# 运行完整数据集处理 ⭐ 推荐
python process_complete_dataset.py

# 运行小数据集处理
python grammar_constrained_decoding.py

# 生成对比报告
python compare_results.py
```

### 3️⃣ 查看结果

```powershell
# 查看统计摘要
Get-Content "result_comp\experiment_summary.json" | ConvertFrom-Json

# 查看第一条样本
Get-Content "result_comp\processed_samples.json" | ConvertFrom-Json | Select-Object -First 1

# 查看文件大小
Get-ChildItem "result_comp\" -File | Format-Table Name, @{Label="Size (KB)"; Expression={[math]::Round($_.Length/1KB, 2)}}
```

---

## 项目结构图

```
experiment/
│
├── 📄 文档
│   ├── README.md
│   ├── QUICK_START.md ⭐
│   ├── PROJECT_DOCUMENTATION.md ⭐
│   ├── COMPLETION_REPORT.md ⭐
│   └── FILE_INDEX.md (本文件)
│
├── 🐍 主要脚本
│   ├── process_complete_dataset.py ⭐ (推荐)
│   ├── grammar_constrained_decoding.py
│   └── compare_results.py
│
├── 📝 配置
│   └── python_grammar.lark
│
├── 📊 结果输出
│   ├── result_comp/ ⭐ 完整数据集结果
│   │   ├── json_schema_outlines.json (0.49 MB)
│   │   ├── processed_samples.json (0.25 MB)
│   │   └── experiment_summary.json (1 KB)
│   │
│   └── results/ (小数据集结果)
│       ├── json_schema_outlines.json
│       ├── processed_samples.json
│       └── experiment_summary.json
│
└── 🔧 工具脚本
    └── run_full_experiment.py
```

---

---

## 关键概念速查

### JSON Schema Outlines
→ 查看: `PROJECT_DOCUMENTATION.md` > 输出格式说明

### 语法验证机制
→ 查看: `PROJECT_DOCUMENTATION.md` > 核心功能说明

### 数据处理管道
→ 查看: `QUICK_START.md` > 数据流

### 文件格式支持
→ 查看: `PROJECT_DOCUMENTATION.md` > 数据格式说明

---

## 常见问题快速链接

| 问题 | 位置 |
|------|------|
| 如何启动项目？ | QUICK_START.md |
| 有什么依赖？ | PROJECT_DOCUMENTATION.md > 环境配置 |
| 输出格式是什么？ | PROJECT_DOCUMENTATION.md > 输出格式 |
| 性能如何？ | COMPLETION_REPORT.md > 实验结果 |
| 如何处理自己的数据？ | PROJECT_DOCUMENTATION.md > 常见问题 |
| PyTorch 失败怎么办？ | PROJECT_DOCUMENTATION.md > 常见问题 |

---

## 版本信息

| 项目 | 版本 | 日期 |
|------|------|------|
| 项目 | 1.0 | 2025年1月 |
| Python | 3.10.1 | - |
| PyTorch | 2.11.0 | - |
| Lark | 1.3.1 | - |

---

🎯 **建议**: 从 QUICK_START.md 开始，5 分钟内即可运行第一个实验！
