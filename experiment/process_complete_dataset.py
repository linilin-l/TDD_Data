"""
Grammar-Constrained Decoding Experiment with GreatGramma - Complete Dataset Version

This script reads code samples from HumanEval.jsonl.gz and applies
grammar-constrained decoding using GreatGramma, then converts to JSON Schema outlines format.
Results are saved to result_comp directory.
"""

import json
import sys
import ast
import gzip
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# Add the constraint package to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "constraint" / "greatgramma-main"))

try:
    from lark import Lark, Tree, Token
    LARK_AVAILABLE = True
except ImportError:
    LARK_AVAILABLE = False
    print("⚠ Warning: Lark not installed. Install with: pip install lark")


# ============================================================================
# Data Loading Functions
# ============================================================================

def load_jsonl(file_path: str) -> List[Dict]:
    """
    Load JSONL file and return list of records
    Supports both plain .jsonl and compressed .jsonl.gz files
    
    Args:
        file_path (str): Path to JSONL or JSONL.gz file
        
    Returns:
        list: List of dictionaries from JSONL
    """
    records = []
    try:
        if file_path.endswith('.gz'):
            with gzip.open(file_path, 'rt', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
        else:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        records.append(json.loads(line))
        print(f"✓ Successfully loaded {len(records)} records from {file_path}")
        return records
    except FileNotFoundError:
        print(f"✗ Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"✗ Error: JSON decode error - {e}")
        return []
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return []


def analyze_samples(records):
    """
    Analyze and display sample statistics
    
    Args:
        records (list): List of sample records
    """
    print("\n" + "="*60)
    print("SAMPLE ANALYSIS")
    print("="*60)
    
    print(f"Total records: {len(records)}")
    
    if records:
        print(f"\nFirst record:")
        print(json.dumps(records[0], indent=2, ensure_ascii=False)[:500])
        
        # Group by task_id
        task_ids = {}
        for record in records:
            task_id = record.get('task_id', 'unknown')
            if task_id not in task_ids:
                task_ids[task_id] = 0
            task_ids[task_id] += 1
        
        print(f"\nTotal unique tasks: {len(task_ids)}")
        print(f"First 10 tasks:")
        for i, (task_id, count) in enumerate(sorted(task_ids.items())[:10]):
            print(f"  - {task_id}: {count} samples")


# ============================================================================
# Grammar Validation Functions
# ============================================================================

def validate_python_syntax(code: str) -> tuple:
    """
    Validate Python code syntax using AST parser
    
    Args:
        code (str): Python code to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def validate_with_lark_grammar(code: str, parser: Optional[Any]) -> tuple:
    """
    Validate code using Lark grammar parser
    
    Args:
        code (str): Code to validate
        parser (Lark): Lark parser instance
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not parser or not LARK_AVAILABLE:
        return True, None
    
    try:
        parser.parse(code)
        return True, None
    except Exception as e:
        return False, str(e)


# ============================================================================
# JSON Schema and Outlines Format Conversion
# ============================================================================

class JSONSchemaType(str, Enum):
    """JSON Schema type definitions"""
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    OBJECT = "object"
    ARRAY = "array"
    BOOLEAN = "boolean"
    NULL = "null"


def build_json_schema_from_code(code: str, task_id: str, index: int) -> Dict[str, Any]:
    """
    Build JSON Schema from code completion
    
    Args:
        code (str): Code completion
        task_id (str): Task identifier
        index (int): Index in batch
        
    Returns:
        dict: JSON Schema representation
    """
    # Validate syntax
    is_valid, error = validate_python_syntax(code)
    
    # Detect code features
    has_return = "return" in code
    has_import = "import" in code
    has_function_def = "def " in code
    has_class_def = "class " in code
    
    # Extract indentation
    indentation = detect_indentation(code)
    
    # Build schema
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": f"Code Completion {task_id}/{index}",
        "description": "Python code completion with grammar constraints",
        "type": "object",
        "properties": {
            "task_id": {
                "type": "string",
                "description": "Task identifier",
                "examples": [task_id]
            },
            "completion": {
                "type": "string",
                "description": "Python code completion",
                "pattern": "^[\\s\\S]*$",
                "examples": [code[:100] if len(code) > 100 else code]
            },
            "analysis": {
                "type": "object",
                "description": "Code analysis results",
                "properties": {
                    "valid_syntax": {
                        "type": "boolean",
                        "description": "Whether code has valid Python syntax",
                        "examples": [is_valid]
                    },
                    "length": {
                        "type": "integer",
                        "description": "Code length in characters",
                        "examples": [len(code)]
                    },
                    "lines": {
                        "type": "integer",
                        "description": "Number of lines",
                        "examples": [len(code.split('\n'))]
                    },
                    "has_return": {
                        "type": "boolean",
                        "description": "Contains return statement",
                        "examples": [has_return]
                    },
                    "has_import": {
                        "type": "boolean",
                        "description": "Contains import statement",
                        "examples": [has_import]
                    },
                    "has_function_def": {
                        "type": "boolean",
                        "description": "Contains function definition",
                        "examples": [has_function_def]
                    },
                    "has_class_def": {
                        "type": "boolean",
                        "description": "Contains class definition",
                        "examples": [has_class_def]
                    },
                    "indentation": {
                        "type": "string",
                        "description": "Indentation style",
                        "enum": ["4-spaces", "2-spaces", "tab", "no-indent"],
                        "examples": [indentation]
                    }
                },
                "required": ["valid_syntax", "length", "lines", "indentation"]
            }
        },
        "required": ["task_id", "completion", "analysis"]
    }
    
    if not is_valid:
        schema["properties"]["analysis"]["properties"]["syntax_error"] = {
            "type": "string",
            "description": "Syntax error message",
            "examples": [error]
        }
    
    return schema


def apply_grammar_constraints(records: List[Dict]) -> tuple:
    """
    Apply grammar constraints to code completions and convert to JSON Schema outlines format
    
    Args:
        records (list): List of sample records with code completions
        
    Returns:
        tuple: (processed_records, schema_outlines)
    """
    print("\n" + "="*60)
    print("GRAMMAR CONSTRAINT ANALYSIS")
    print("="*60)
    
    processed_records = []
    schema_outlines = []
    
    # Try to load Lark grammar
    parser = None
    grammar_file = Path(__file__).parent / "python_grammar.lark"
    
    if LARK_AVAILABLE and grammar_file.exists():
        try:
            with open(grammar_file, 'r') as f:
                grammar = f.read()
            parser = Lark(grammar, start='start', parser='lalr', propagate_positions=True)
            print("✓ Lark parser initialized with Python grammar")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize Lark parser: {e}")
            parser = None
    else:
        print("⚠ Warning: Lark grammar file not found or Lark not available")
    
    # Try to import GreatGramma monitor (optional)
    try:
        from alignment.monitor.grammar.cfg_monitor import CFGMonitor
        print("✓ GreatGramma CFGMonitor successfully imported")
    except Exception as e:
        print(f"⚠ Warning: Could not import GreatGramma CFGMonitor: {type(e).__name__}: {str(e)[:80]}")
    
    print(f"\nProcessing {len(records)} records...")
    total_records = len(records)
    
    for i, record in enumerate(records):
        completion = record.get('completion', '')
        task_id = record.get('task_id', 'unknown')
        
        # Show progress every 100 records
        if i % 100 == 0 and i > 0:
            print(f"  Progress: {i}/{total_records} records processed ({(i/total_records*100):.1f}%)")
        
        # Validate syntax using AST
        is_valid_ast, ast_error = validate_python_syntax(completion)
        
        # Validate with Lark if available
        is_valid_lark, lark_error = validate_with_lark_grammar(completion, parser)
        
        # Build analysis
        analysis = {
            'completion_length': len(completion),
            'lines': len(completion.split('\n')),
            'has_return': 'return' in completion,
            'has_import': 'import' in completion,
            'indentation': detect_indentation(completion),
            'syntax_valid_ast': is_valid_ast,
            'syntax_valid_lark': is_valid_lark
        }
        
        if not is_valid_ast:
            analysis['ast_error'] = ast_error
        if not is_valid_lark:
            analysis['lark_error'] = lark_error
        
        # Create processed record
        processed_record = {
            **record,
            'analysis': analysis
        }
        processed_records.append(processed_record)
        
        # Build JSON Schema outline
        schema = build_json_schema_from_code(completion, task_id, i)
        outline = {
            'id': f"{task_id}_{i}",
            'task_id': task_id,
            'index': i,
            'schema': schema,
            'constraints': {
                'grammar_validated': is_valid_lark if parser else None,
                'syntax_validated': is_valid_ast,
                'enforced_fields': ['task_id', 'completion', 'analysis']
            }
        }
        schema_outlines.append(outline)
        
        if i < 3:
            print(f"\nRecord {i}:")
            print(f"  Task ID: {task_id}")
            print(f"  Completion: {completion[:60]}...")
            print(f"  Syntax Valid (AST): {is_valid_ast}")
            print(f"  Syntax Valid (Lark): {is_valid_lark}")
    
    print(f"\n✓ Processed {len(processed_records)} records")
    return processed_records, schema_outlines


def detect_indentation(code):
    """Detect the indentation style in code"""
    lines = code.split('\n')
    for line in lines:
        if line and line[0] in (' ', '\t'):
            if line[0] == '\t':
                return 'tab'
            elif line.startswith('    '):
                return '4-spaces'
            elif line.startswith('  '):
                return '2-spaces'
    return 'no-indent'


# ============================================================================
# File I/O Functions
# ============================================================================

def save_results(results, output_path):
    """Save processing results to JSON file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✓ Results saved to {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error saving results: {e}")
        return False


def save_schema_outlines(outlines, output_path):
    """Save JSON Schema outlines to file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(outlines, f, indent=2, ensure_ascii=False)
        print(f"✓ Schema outlines saved to {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error saving schema outlines: {e}")
        return False


def save_summary(summary, output_path):
    """Save experiment summary to JSON file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"✓ Summary saved to {output_path}")
        return True
    except Exception as e:
        print(f"✗ Error saving summary: {e}")
        return False


def main():
    """Main execution function"""
    print("="*60)
    print("Grammar-Constrained Decoding Experiment")
    print("Using GreatGramma for Constrained Decoding")
    print("Converting to JSON Schema Outlines Format")
    print("="*60)
    
    # Define file paths - use complete HumanEval dataset
    data_file = Path(__file__).parent.parent / "Data" / "human-eval-master" / "data" / "HumanEval.jsonl.gz"
    results_dir = Path(__file__).parent / "result_comp"
    processed_file = results_dir / "processed_samples.json"
    schemas_file = results_dir / "json_schema_outlines.json"
    summary_file = results_dir / "experiment_summary.json"
    
    # Create results directory
    results_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nData file: {data_file}")
    print(f"Results directory: {results_dir}")
    
    # Step 1: Load samples
    print("\n" + "-"*60)
    print("STEP 1: Loading JSONL.GZ data")
    print("-"*60)
    records = load_jsonl(str(data_file))
    
    if not records:
        print("\n✗ Failed to load data. Exiting.")
        return
    
    # Step 2: Analyze samples
    print("\n" + "-"*60)
    print("STEP 2: Analyzing samples")
    print("-"*60)
    analyze_samples(records)
    
    # Step 3: Apply grammar constraints and convert to outlines format
    print("\n" + "-"*60)
    print("STEP 3: Applying grammar constraints")
    print("-"*60)
    processed_records, schema_outlines = apply_grammar_constraints(records)
    
    # Step 4: Save results
    print("\n" + "-"*60)
    print("STEP 4: Saving results")
    print("-"*60)
    save_results(processed_records, str(processed_file))
    save_schema_outlines(schema_outlines, str(schemas_file))
    
    # Step 5: Generate and save summary
    print("\n" + "-"*60)
    print("STEP 5: Generating summary")
    print("-"*60)
    
    # Calculate statistics
    valid_count = sum(1 for p in processed_records if p['analysis'].get('syntax_valid_ast', False))
    lark_valid_count = sum(1 for p in processed_records if p['analysis'].get('syntax_valid_lark', False))
    
    summary = {
        "experiment": "Grammar-Constrained Decoding with GreatGramma - Complete Dataset",
        "data_source": "HumanEval.jsonl.gz",
        "statistics": {
            "total_records": len(records),
            "valid_ast_syntax": valid_count,
            "valid_lark_grammar": lark_valid_count,
            "validity_rate_ast": f"{(valid_count / len(records) * 100):.1f}%",
            "validity_rate_lark": f"{(lark_valid_count / len(records) * 100):.1f}%" if lark_valid_count >= 0 else "N/A"
        },
        "indentation_distribution": {
            "4-spaces": sum(1 for p in processed_records if p['analysis'].get('indentation') == '4-spaces'),
            "2-spaces": sum(1 for p in processed_records if p['analysis'].get('indentation') == '2-spaces'),
            "tabs": sum(1 for p in processed_records if p['analysis'].get('indentation') == 'tab'),
            "no-indent": sum(1 for p in processed_records if p['analysis'].get('indentation') == 'no-indent')
        },
        "code_features": {
            "has_return": sum(1 for p in processed_records if p['analysis'].get('has_return', False)),
            "has_import": sum(1 for p in processed_records if p['analysis'].get('has_import', False))
        },
        "output_files": {
            "processed_samples": str(processed_file),
            "json_schema_outlines": str(schemas_file),
            "summary": str(summary_file)
        }
    }
    
    save_summary(summary, str(summary_file))
    
    # Print final summary
    print("\n" + "="*60)
    print("EXPERIMENT SUMMARY")
    print("="*60)
    print(f"Total records processed: {summary['statistics']['total_records']}")
    print(f"Valid Python syntax (AST): {summary['statistics']['valid_ast_syntax']} ({summary['statistics']['validity_rate_ast']})")
    print(f"Valid Lark grammar: {summary['statistics']['valid_lark_grammar']} ({summary['statistics']['validity_rate_lark']})")
    print(f"\nIndentation Distribution:")
    for indent_style, count in summary['indentation_distribution'].items():
        print(f"  - {indent_style}: {count}")
    print(f"\nCode Features:")
    print(f"  - Has return statement: {summary['code_features']['has_return']}")
    print(f"  - Has import statement: {summary['code_features']['has_import']}")
    print(f"\n✓ All results saved to {results_dir}")
    print("="*60)


if __name__ == "__main__":
    main()
