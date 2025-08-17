#!/usr/bin/env python3
"""
Debug script to identify mismatches between model keys in size data and Gradio lookup keys.
"""

import json
import os
from Downloader_Gradio_App import models_structure, MODEL_SIZES_FILE

def load_size_data():
    """Load the model size data from JSON file."""
    if not os.path.exists(MODEL_SIZES_FILE):
        print(f"ERROR: {MODEL_SIZES_FILE} not found. Run fetch_model_sizes.py first.")
        return None
    
    try:
        with open(MODEL_SIZES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Could not load {MODEL_SIZES_FILE}: {e}")
        return None

def analyze_model_keys():
    """Analyze model keys and find mismatches."""
    size_data = load_size_data()
    if not size_data:
        return
    
    print("=== MODEL KEY ANALYSIS ===\n")
    
    # Get all keys from size data
    size_keys = set(size_data.get("models", {}).keys())
    print(f"Total models in size data: {len(size_keys)}")
    
    # Get all keys that should be generated from models_structure
    expected_keys = set()
    missing_keys = []
    
    for cat_name, cat_data in models_structure.items():
        if "sub_categories" in cat_data:
            for sub_cat_name, sub_cat_data in cat_data["sub_categories"].items():
                for model_info in sub_cat_data.get("models", []):
                    model_name = model_info.get("name", "Unknown")
                    expected_key = f"{cat_name}::{sub_cat_name}::{model_name}"
                    expected_keys.add(expected_key)
                    
                    if expected_key not in size_keys:
                        missing_keys.append({
                            "key": expected_key,
                            "model_name": model_name,
                            "category": cat_name,
                            "sub_category": sub_cat_name,
                            "repo_id": model_info.get("repo_id"),
                            "filename": model_info.get("filename_in_repo"),
                            "is_snapshot": model_info.get("is_snapshot", False)
                        })
    
    print(f"Expected models from structure: {len(expected_keys)}")
    print(f"Missing from size data: {len(missing_keys)}")
    
    # Find keys in size data that aren't in expected
    extra_keys = size_keys - expected_keys
    print(f"Extra keys in size data: {len(extra_keys)}")
    
    # Show missing keys
    if missing_keys:
        print("\n=== MISSING KEYS (not in size data) ===")
        for missing in missing_keys:
            print(f"Key: {missing['key']}")
            print(f"  Model: {missing['model_name']}")
            print(f"  Category: {missing['category']} -> {missing['sub_category']}")
            print(f"  Repo: {missing['repo_id']}")
            print(f"  File: {missing['filename']}")
            print(f"  Is Snapshot: {missing['is_snapshot']}")
            print()
    
    # Show extra keys
    if extra_keys:
        print("\n=== EXTRA KEYS (in size data but not expected) ===")
        for extra_key in sorted(extra_keys):
            print(f"Key: {extra_key}")
            size_info = size_data["models"][extra_key]
            print(f"  Size: {size_info.get('size_gb', 0):.2f} GB")
            if size_info.get('error'):
                print(f"  Error: {size_info['error']}")
            print()
    
    # Search for specific model mentioned by user
    search_term = "UMT5 XXL FP16"
    print(f"\n=== SEARCHING FOR '{search_term}' ===")
    
    found_in_structure = []
    found_in_size_data = []
    
    # Search in models_structure
    for cat_name, cat_data in models_structure.items():
        if "sub_categories" in cat_data:
            for sub_cat_name, sub_cat_data in cat_data["sub_categories"].items():
                for model_info in sub_cat_data.get("models", []):
                    model_name = model_info.get("name", "Unknown")
                    if search_term.lower() in model_name.lower():
                        found_in_structure.append({
                            "name": model_name,
                            "category": cat_name,
                            "sub_category": sub_cat_name,
                            "key": f"{cat_name}::{sub_cat_name}::{model_name}"
                        })
    
    # Search in size data
    for key in size_keys:
        if search_term.lower() in key.lower():
            found_in_size_data.append(key)
    
    print(f"Found {len(found_in_structure)} matches in models_structure:")
    for match in found_in_structure:
        print(f"  - {match['name']}")
        print(f"    Category: {match['category']} -> {match['sub_category']}")
        print(f"    Key: {match['key']}")
        print(f"    In size data: {'YES' if match['key'] in size_keys else 'NO'}")
        print()
    
    print(f"Found {len(found_in_size_data)} matches in size data:")
    for key in found_in_size_data:
        print(f"  - {key}")
    
    print("\n=== SUMMARY ===")
    print(f"Total models in structure: {len(expected_keys)}")
    print(f"Total models in size data: {len(size_keys)}")
    print(f"Missing from size data: {len(missing_keys)}")
    print(f"Extra in size data: {len(extra_keys)}")

if __name__ == "__main__":
    analyze_model_keys() 