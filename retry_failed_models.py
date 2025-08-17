#!/usr/bin/env python3
"""
Retry Failed Models Script for SwarmUI Model Downloader

This script retries fetching sizes for models that previously failed
and provides detailed error information.
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional

try:
    from huggingface_hub import HfFileSystem
    from huggingface_hub.utils import HfHubHTTPError, HFValidationError
except ImportError:
    print("huggingface_hub not found. Please install it: pip install huggingface_hub")
    sys.exit(1)

# Set Hugging Face token for authentication
HF_TOKEN = "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"
os.environ["HUGGING_FACE_HUB_TOKEN"] = HF_TOKEN

MODEL_SIZES_FILE = "model_sizes.json"

def bytes_to_gb(bytes_size: int) -> float:
    """Convert bytes to GB with 2 decimal precision."""
    return round(bytes_size / (1024 ** 3), 2)

def get_file_size_from_hf_with_details(repo_id: str, filename: str = None) -> tuple[Optional[int], str]:
    """
    Get file size from Hugging Face Hub with detailed error reporting.
    
    Returns:
        Tuple of (size_in_bytes, error_message)
    """
    try:
        # Initialize with token for authentication
        fs = HfFileSystem(token=HF_TOKEN)
        
        if filename:
            # Get size of specific file
            file_path = f"{repo_id}/{filename}"
            try:
                file_info = fs.info(file_path)
                size = file_info.get('size', 0)
                return size, "Success"
            except Exception as e:
                return None, f"File access error: {str(e)}"
        else:
            # Get total size of repository
            try:
                total_size = 0
                repo_files = fs.glob(f"{repo_id}/*", detail=True)
                for file_path, file_info in repo_files.items():
                    if file_info.get('type') == 'file':
                        total_size += file_info.get('size', 0)
                return total_size, "Success"
            except Exception as e:
                return None, f"Repository access error: {str(e)}"
                
    except HfHubHTTPError as e:
        return None, f"HTTP Error: {str(e)}"
    except HFValidationError as e:
        return None, f"Validation Error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def load_size_data() -> Optional[Dict]:
    """Load existing size data."""
    try:
        if os.path.exists(MODEL_SIZES_FILE):
            with open(MODEL_SIZES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        print(f"Error loading size data: {e}")
        return None

def save_size_data(size_data: Dict) -> bool:
    """Save updated size data."""
    try:
        with open(MODEL_SIZES_FILE, 'w', encoding='utf-8') as f:
            json.dump(size_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving size data: {e}")
        return False

def find_failed_models(size_data: Dict) -> List[Dict]:
    """Find all models that failed to fetch sizes."""
    failed_models = []
    
    if "models" in size_data:
        for model_key, model_info in size_data["models"].items():
            if model_info.get("error") or model_info.get("size_bytes", 0) == 0:
                failed_models.append({
                    "key": model_key,
                    "info": model_info
                })
    
    return failed_models

def retry_failed_models():
    """Main function to retry failed models."""
    print("SwarmUI Model Size Retry Tool")
    print("=" * 50)
    print(f"🔑 Using Hugging Face token: {HF_TOKEN[:10]}...{HF_TOKEN[-4:]}")
    print("=" * 50)
    
    # Load existing data
    size_data = load_size_data()
    if not size_data:
        print("Error: No existing size data found. Please run fetch_model_sizes.py first.")
        return
    
    # Find failed models
    failed_models = find_failed_models(size_data)
    
    if not failed_models:
        print("Great! No failed models found. All models have sizes.")
        return
    
    print(f"Found {len(failed_models)} failed models:")
    print("-" * 30)
    
    for i, failed_model in enumerate(failed_models, 1):
        model_info = failed_model["info"]
        print(f"{i}. {model_info.get('name', 'Unknown')}")
        print(f"   Repository: {model_info.get('repo_id', 'Unknown')}")
        print(f"   File: {model_info.get('filename', 'Full repo')}")
        if model_info.get("error"):
            print(f"   Previous error: {model_info['error']}")
        print()
    
    response = input("Do you want to retry fetching these models? (y/N): ")
    if response.lower() != 'y':
        print("Exiting without retrying.")
        return
    
    print("\nRetrying failed models...")
    print("-" * 30)
    
    success_count = 0
    still_failed_count = 0
    
    for i, failed_model in enumerate(failed_models, 1):
        model_key = failed_model["key"]
        model_info = failed_model["info"]
        model_name = model_info.get('name', 'Unknown')
        repo_id = model_info.get('repo_id')
        filename = model_info.get('filename')
        is_snapshot = model_info.get('is_snapshot', False)
        
        print(f"\n[{i}/{len(failed_models)}] Retrying: {model_name}")
        
        if not repo_id:
            print("  ❌ Error: No repository ID")
            continue
        
        # Retry fetching
        if is_snapshot:
            size_bytes, error_msg = get_file_size_from_hf_with_details(repo_id)
        else:
            size_bytes, error_msg = get_file_size_from_hf_with_details(repo_id, filename)
        
        if size_bytes is not None and error_msg == "Success":
            # Success! Update the data
            size_data["models"][model_key].update({
                "size_bytes": size_bytes,
                "size_gb": bytes_to_gb(size_bytes)
            })
            # Remove error field if it exists
            if "error" in size_data["models"][model_key]:
                del size_data["models"][model_key]["error"]
            
            print(f"  ✅ Success: {bytes_to_gb(size_bytes)} GB")
            success_count += 1
        else:
            # Still failed
            size_data["models"][model_key].update({
                "size_bytes": 0,
                "size_gb": 0.0,
                "error": f"Retry failed: {error_msg}"
            })
            print(f"  ❌ Still failed: {error_msg}")
            still_failed_count += 1
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Update timestamp
    size_data["fetch_timestamp"] = time.time()
    size_data["fetch_date"] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Save updated data
    if save_size_data(size_data):
        print(f"\n" + "=" * 50)
        print("RETRY SUMMARY:")
        print(f"✅ Successfully fixed: {success_count} models")
        print(f"❌ Still failed: {still_failed_count} models")
        print(f"📁 Updated data saved to: {MODEL_SIZES_FILE}")
        
        if success_count > 0:
            print("\n🎉 Some models were fixed! Restart your application to see the updated sizes.")
        
        if still_failed_count > 0:
            print(f"\n⚠️  {still_failed_count} models are still failing. Common reasons:")
            print("   • Repository is private or requires authentication")
            print("   • File doesn't exist in the repository")
            print("   • Repository has been moved or deleted")
            print("   • Network connectivity issues")
    else:
        print("❌ Error: Could not save updated data.")

def check_specific_model():
    """Check a specific model manually."""
    print("\nManual Model Check")
    print("-" * 20)
    
    repo_id = input("Enter repository ID (e.g., OwlMaster/Some_best_SDXL): ").strip()
    if not repo_id:
        print("No repository ID provided.")
        return
    
    filename = input("Enter filename (or press Enter for full repo): ").strip()
    filename = filename if filename else None
    
    print(f"\nChecking: {repo_id}" + (f"/{filename}" if filename else " (full repo)"))
    
    size_bytes, error_msg = get_file_size_from_hf_with_details(repo_id, filename)
    
    if size_bytes is not None:
        print(f"✅ Success: {bytes_to_gb(size_bytes)} GB ({size_bytes:,} bytes)")
    else:
        print(f"❌ Failed: {error_msg}")

if __name__ == "__main__":
    try:
        retry_failed_models()
        
        # Offer manual check option
        print("\n" + "-" * 50)
        response = input("Do you want to manually check a specific model? (y/N): ")
        if response.lower() == 'y':
            check_specific_model()
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}") 