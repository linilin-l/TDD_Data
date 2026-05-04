# 🚀 快速开始指南

## 一键启动

### 步骤 1: 激活虚拟环境

```powershell
cd "d:\新建文件夹\A SCNU\项目\AI教育\TDD"

# 激活 alignment_env 虚拟环境
& "alignment_env\Scripts\Activate.ps1"
```

你会看到提示符左边显示 `(alignment_env)`，表示虚拟环境已激活。

### 步骤 2: 进入实验目录

```powershell
cd experiment
```

### 步骤 3: 运行完整数据集处理（推荐）

```powershell
python process_complete_dataset.py
```

**预期输出:**
```
============================================================
Grammar-Constrained Decoding Experiment
...
Total records processed: 164
Valid Python syntax (AST): 164 (100.0%)
Valid Lark grammar: 164 (100.0%)
✓ All results saved to D:\...\result_comp
============================================================
```

**结果文件:**
- `result_comp/processed_samples.json` - 处理后的代码样本
- `result_comp/json_schema_outlines.json` - JSON Schema Outlines 格式（主要输出）
- `result_comp/experiment_summary.json` - 实验统计总结

---

## 查看结果

### 方法 1: 查看实验总结

```powershell
# 查看统计摘要
Get-Content "result_comp\experiment_summary.json" | ConvertFrom-Json | Format-List
```

### 方法 2: 查看处理后的样本

```powershell
# 查看处理后的第一条样本
Get-Content "result_comp\processed_samples.json" | ConvertFrom-Json | Select-Object -First 1
```

### 方法 3: 对比两个数据集

```powershell
python compare_results.py
```

---

## 目录结构速查

```
experiment/
├── process_complete_dataset.py ⭐ 主脚本
├── python_grammar.lark           # Python 语法定义
├── result_comp/                  ⭐ 结果输出
│   ├── processed_samples.json
│   ├── json_schema_outlines.json
│   └── experiment_summary.json
└── results/                      # 小数据集结果
```

---

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `python process_complete_dataset.py` | 处理完整数据集（164 条记录） |
| `python grammar_constrained_decoding.py` | 处理小数据集（6 条记录） |
| `python compare_results.py` | 对比两个数据集的结果 |

---

## 数据流

```
HumanEval.jsonl.gz (完整数据集，164 条)
         ↓
  load_jsonl() 解压 & 加载
         ↓
  analyze_samples() 分析样本
         ↓
  apply_grammar_constraints() 语法验证
         ├─ AST 验证 (Python 标准库)
         └─ Lark 验证 (python_grammar.lark)
         ↓
  build_json_schema_from_code() 生成 Schema
         ↓
result_comp/
├── processed_samples.json
├── json_schema_outlines.json ⭐ 主要输出
└── experiment_summary.json
```

---

## 输出格式示例

### JSON Schema Outlines（fragment）

```json
{
  "id": "HumanEval/0_0",
  "task_id": "HumanEval/0",
  "schema": {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
      "task_id": {"type": "string"},
      "completion": {"type": "string"},
      "analysis": {
        "type": "object",
        "properties": {
          "valid_syntax": {"type": "boolean"},
          "indentation": {"type": "string"},
          ...
        }
      }
    }
  }
}
```

---

## 故障排除

### 问题 1: ModuleNotFoundError: No module named 'lark'

**解决:**
```powershell
pip install lark
```

### 问题 2: 虚拟环境激活失败

**解决:**
```powershell
# 查看执行策略
Get-ExecutionPolicy

# 如需修改
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题 3: 文件权限错误

**解决:**
```powershell
# 以管理员身份运行 PowerShell 并重试
```

---

## 下一步

✅ 已完成: 数据加载、语法验证、JSON Schema 生成  
⏳ 可扩展: 自定义语法规则、LLM 集成、并行处理  

---

**提示**: 所有脚本都支持修改 `data_file` 路径来处理你自己的数据集！

需要帮助？参考 `PROJECT_DOCUMENTATION.md` 获取更详细的信息。
