#!/usr/bin/env python3
"""Debug script to check model name mismatches between structure and size data."""

import json
import sys
sys.path.append('.')
from Downloader_Gradio_App import load_model_sizes, models_structure, size_data

# Load the size data
load_model_sizes()

print("=== DEBUGGING MODEL SIZE MISMATCHES ===")
print()

# Check UMT5 models specifically
print("UMT5 Models in Structure:")
umt5_models = models_structure['Text Encoder Models']['sub_categories']['UMT5 XXL Models']['models']
for model in umt5_models:
    print(f"  - {model['name']}")

print("\nUMT5 Keys in Size Data:")
for key in size_data['models'].keys():
    if 'UMT5' in key:
        print(f"  - {key}")

print("\n=== CHECKING SPECIFIC MODEL LOOKUPS ===")

# Test specific model lookups
test_model = "UMT5 XXL FP16 (Save As default for SwarmUI)"
expected_key = f"Text Encoder Models::UMT5 XXL Models::{test_model}"
print(f"\nTesting model: {test_model}")
print(f"Expected key: {expected_key}")
print(f"Key exists in size data: {expected_key in size_data['models']}")

if expected_key in size_data['models']:
    model_info = size_data['models'][expected_key]
    print(f"Size data: {model_info}")
else:
    print("Available keys containing 'UMT5' and 'FP16':")
    for key in size_data['models'].keys():
        if 'UMT5' in key and 'FP16' in key:
            print(f"  - {key}")

print("\n=== CHECKING ALL MISMATCHES ===")
mismatches = []

# Check all categories
for cat_name, cat_data in models_structure.items():
    if "sub_categories" in cat_data:
        for sub_cat_name, sub_cat_data in cat_data["sub_categories"].items():
            for model_info in sub_cat_data.get("models", []):
                model_name = model_info.get("name", "")
                model_key = f"{cat_name}::{sub_cat_name}::{model_name}"
                
                if model_key not in size_data['models']:
                    mismatches.append({
                        'category': cat_name,
                        'subcategory': sub_cat_name,
                        'model_name': model_name,
                        'expected_key': model_key
                    })

if mismatches:
    print(f"Found {len(mismatches)} mismatches:")
    for i, mismatch in enumerate(mismatches[:10]):  # Show first 10
        print(f"  {i+1}. {mismatch['model_name']}")
        print(f"     Expected: {mismatch['expected_key']}")
        # Try to find similar keys
        similar_keys = [k for k in size_data['models'].keys() if mismatch['model_name'][:20] in k]
        if similar_keys:
            print(f"     Similar keys found: {similar_keys[:2]}")
        print()
else:
    print("No mismatches found!") 