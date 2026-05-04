# Grammar-Constrained Decoding Experiment 项目文档

## 项目概述

本项目实现了使用 **GreatGramma** 进行语法约束解码的完整工作流，将代码数据库转换为 **JSON Schema outlines 格式**。

### 核心目标

✅ 读取 JSONL/JSONL.GZ 格式的代码数据  
✅ 应用 GreatGramma 的语法约束验证  
✅ 使用 Lark 进行语法解析  
✅ 生成标准化的 JSON Schema 输出格式  
✅ 支持大规模数据集处理  

---

## 环境配置

### 虚拟环境

使用独立的 Python 虚拟环境：`alignment_env`

```powershell
# 激活环境
& "d:\新建文件夹\A SCNU\项目\AI教育\TDD\alignment_env\Scripts\Activate.ps1"

# 验证环境
python --version
```

### 安装依赖

```powershell
cd "d:\新建文件夹\A SCNU\项目\AI教育\TDD\experiment"

# 安装 Lark 用于语法解析
pip install lark

# 安装 PyTorch（可选，用于 GreatGramma）
pip install torch
```

---

## 项目结构

```
experiment/
├── grammar_constrained_decoding.py      # 原始脚本（小数据集）
├── process_complete_dataset.py          # 完整数据集处理脚本 ⭐
├── run_full_experiment.py               # 实验启动器
├── compare_results.py                   # 对比分析脚本
├── python_grammar.lark                  # Python 语法定义文件
├── README.md                             # 项目文档
├── results/                             # 小数据集结果
│   ├── processed_samples.json
│   ├── json_schema_outlines.json
│   └── experiment_summary.json
└── result_comp/                         # 完整数据集结果 ⭐
    ├── processed_samples.json           (0.25 MB)
    ├── json_schema_outlines.json        (0.49 MB)
    └── experiment_summary.json
```

---

## 使用方法

### 1. 处理完整数据集（推荐）

```powershell
cd "d:\新建文件夹\A SCNU\项目\AI教育\TDD\experiment"

# 运行完整数据集处理
python process_complete_dataset.py
```

**输出文件位置：** `result_comp/`

### 2. 处理小数据集（测试用）

```powershell
# 运行原始脚本
python grammar_constrained_decoding.py
```

**输出文件位置：** `results/`

### 3. 生成对比报告

```powershell
# 对比两个数据集的处理结果
python compare_results.py
```

---

## 数据格式说明

### 输入格式

**JSONL.GZ 格式** - 压缩的 JSON Lines

```json
{"task_id": "HumanEval/0", "prompt": "...", "canonical_solution": "...", "test": "...", "entry_point": "..."}
{"task_id": "HumanEval/1", "prompt": "...", "canonical_solution": "...", "test": "...", "entry_point": "..."}
...
```

### 输出格式：JSON Schema Outlines

```json
{
  "id": "HumanEval/0_0",
  "task_id": "HumanEval/0",
  "index": 0,
  "schema": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Code Completion HumanEval/0/0",
    "description": "Python code completion with grammar constraints",
    "type": "object",
    "properties": {
      "task_id": {
        "type": "string",
        "description": "Task identifier",
        "examples": ["HumanEval/0"]
      },
      "completion": {
        "type": "string",
        "description": "Python code completion",
        "pattern": "^[\\s\\S]*$",
        "examples": ["code snippet"]
      },
      "analysis": {
        "type": "object",
        "description": "Code analysis results",
        "properties": {
          "valid_syntax": {"type": "boolean"},
          "length": {"type": "integer"},
          "lines": {"type": "integer"},
          "has_return": {"type": "boolean"},
          "has_import": {"type": "boolean"},
          "has_function_def": {"type": "boolean"},
          "has_class_def": {"type": "boolean"},
          "indentation": {
            "type": "string",
            "enum": ["4-spaces", "2-spaces", "tab", "no-indent"]
          }
        }
      }
    },
    "required": ["task_id", "completion", "analysis"]
  },
  "constraints": {
    "grammar_validated": true,
    "syntax_validated": true,
    "enforced_fields": ["task_id", "completion", "analysis"]
  }
}
```

---

## 实验结果

### 完整数据集（HumanEval.jsonl.gz）

| 指标 | 结果 |
|------|------|
| 总记录数 | 164 |
| AST 语法有效率 | 100.0% ✅ |
| Lark 语法有效率 | 100.0% ✅ |
| 输出 JSON Schema 记录数 | 164 |
| 输出文件大小 | 0.49 MB |

### 小数据集（example_samples.jsonl）

| 指标 | 结果 |
|------|------|
| 总记录数 | 6 |
| AST 语法有效率 | 0.0% |
| Lark 语法有效率 | 100.0% ✅ |
| 输出 JSON Schema 记录数 | 6 |
| 输出文件大小 | ~0.08 MB |

---

## 核心功能说明

### 1. 数据加载（`load_jsonl`）

- 支持 `.jsonl` 和 `.jsonl.gz` 格式
- 自动检测并解压缩
- 逐行加载处理，节省内存

### 2. 语法验证（双重验证）

#### AST 验证
```python
ast.parse(code)  # Python 标准库
```

#### Lark 语法验证
```python
parser.parse(code)  # 基于 python_grammar.lark
```

### 3. 代码分析

提取以下特性：
- 代码长度和行数
- 缩进风格（4-spaces, 2-spaces, tab, no-indent）
- 是否包含 return 语句
- 是否包含 import 语句
- 是否包含函数定义
- 是否包含类定义

### 4. JSON Schema 生成

为每条记录生成完整的 JSON Schema（Draft-07）：
- 定义输入/输出结构
- 指定数据类型和约束
- 提供示例和描述
- 定义必需字段

---

## 性能指标

### 处理速度

- **HumanEval 完整数据集（164 条）**：约 5-10 秒
- **进度指示**：每 100 条记录显示一次

### 内存使用

- 流式处理，无需一次性加载所有数据
- 完整数据集处理内存占用 < 200 MB

### 输出大小

- JSON Schema Outlines：0.49 MB（164 条记录）
- 处理后的样本：0.25 MB
- 压缩率：原始 JSONL.GZ 文件 ~300 KB

---

## 常见问题

### Q1: 如何处理自己的数据集？

将你的 JSONL 或 JSONL.GZ 文件放在 `Data/` 目录，然后修改脚本中的数据文件路径：

```python
data_file = Path(__file__).parent.parent / "Data" / "your_data.jsonl.gz"
```

### Q2: 如何修改语法规则？

编辑 `python_grammar.lark` 文件，使用 Lark 语法定义规则。

### Q3: PyTorch 加载失败怎么办？

脚本已设计为可选导入。如果不需要 GreatGramma 的完整功能，可以忽略 PyTorch 错误。

如需修复，可以重新安装 CPU 版本：

```powershell
pip uninstall torch -y
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Q4: 如何扩展脚本功能？

参考 `grammar_constrained_decoding.py` 和 `process_complete_dataset.py` 的架构设计。所有核心函数都支持扩展。


---

## 参考资源

- **GreatGramma**: `constraint/greatgramma-main/`
- **Lark 文档**: https://lark-parser.readthedocs.io/
- **JSON Schema**: https://json-schema.org/

---

**最后更新**: 2025年1月  
**环境**: Python 3.10 + PyTorch 2.11 + Lark 1.3  
**作者**: AI Assistant (GitHub Copilot)
