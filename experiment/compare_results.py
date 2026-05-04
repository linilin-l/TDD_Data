#!/usr/bin/env python3
"""
Comparison Report: Small Dataset vs Complete Dataset

Generates a comparison report between example_samples.json and complete HumanEval results.
"""

import json
from pathlib import Path

def load_json(file_path):
    """Load JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_comparison():
    """Generate comparison report"""
    base_dir = Path(__file__).parent
    
    # Load both summaries
    small_summary = load_json(base_dir / "results" / "experiment_summary.json")
    complete_summary = load_json(base_dir / "result_comp" / "experiment_summary.json")
    
    print("\n" + "="*70)
    print("EXPERIMENT COMPARISON REPORT")
    print("Small Dataset vs Complete Dataset")
    print("="*70)
    
    print("\n📊 DATASET SIZE COMPARISON")
    print("-" * 70)
    print(f"Small Dataset (example_samples)    : {small_summary['statistics']['total_records']:>4} records")
    print(f"Complete Dataset (HumanEval)        : {complete_summary['statistics']['total_records']:>4} records")
    print(f"Growth Factor                       : {complete_summary['statistics']['total_records'] / small_summary['statistics']['total_records']:.1f}x")
    
    print("\n✅ SYNTAX VALIDITY COMPARISON")
    print("-" * 70)
    print(f"{'Metric':<40} {'Small':<15} {'Complete':<15}")
    print("-" * 70)
    
    small_ast_rate = small_summary['statistics']['validity_rate_ast']
    complete_ast_rate = complete_summary['statistics']['validity_rate_ast']
    print(f"{'AST Syntax Validity':<40} {small_ast_rate:<15} {complete_ast_rate:<15}")
    
    small_lark_rate = small_summary['statistics']['validity_rate_lark']
    complete_lark_rate = complete_summary['statistics']['validity_rate_lark']
    print(f"{'Lark Grammar Validity':<40} {small_lark_rate:<15} {complete_lark_rate:<15}")
    
    print("\n📐 INDENTATION DISTRIBUTION")
    print("-" * 70)
    print(f"{'Indentation Style':<40} {'Small':<15} {'Complete':<15}")
    print("-" * 70)
    
    for style in ['4-spaces', '2-spaces', 'tabs', 'no-indent']:
        small_count = small_summary['indentation_distribution'].get(style, 0)
        complete_count = complete_summary['indentation_distribution'].get(style, 0)
        print(f"{style:<40} {small_count:<15} {complete_count:<15}")
    
    print("\n🔧 CODE FEATURES")
    print("-" * 70)
    print(f"{'Feature':<40} {'Small':<15} {'Complete':<15}")
    print("-" * 70)
    
    small_return = small_summary['code_features']['has_return']
    complete_return = complete_summary['code_features']['has_return']
    print(f"{'Has Return Statement':<40} {small_return:<15} {complete_return:<15}")
    
    small_import = small_summary['code_features']['has_import']
    complete_import = complete_summary['code_features']['has_import']
    print(f"{'Has Import Statement':<40} {small_import:<15} {complete_import:<15}")
    
    print("\n" + "="*70)
    print("✓ Comparison report generated successfully!")
    print("="*70)

if __name__ == "__main__":
    generate_comparison()
