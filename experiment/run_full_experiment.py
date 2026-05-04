#!/usr/bin/env python3
"""
Run Grammar-Constrained Decoding Experiment on Complete HumanEval Dataset

This script processes the complete HumanEval.jsonl.gz dataset and generates
JSON Schema outlines format results. Results are saved to result_comp directory.
"""

import sys
from pathlib import Path

# Import the main module
sys.path.insert(0, str(Path(__file__).parent))
from grammar_constrained_decoding import main

if __name__ == "__main__":
    print("\n" + "="*70)
    print("FULL DATASET EXPERIMENT")
    print("Processing: HumanEval.jsonl.gz (Complete Dataset)")
    print("="*70)
    main()
