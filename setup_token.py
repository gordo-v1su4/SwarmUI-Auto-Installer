#!/usr/bin/env python3
"""
Setup Hugging Face Token for SwarmUI Model Downloader

This script sets up the Hugging Face token as an environment variable
for authentication with the Hugging Face Hub.
"""

import os

# Your Hugging Face token
HF_TOKEN = "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"

# Set the environment variable
os.environ["HUGGING_FACE_HUB_TOKEN"] = HF_TOKEN

print("✅ Hugging Face token has been set!")
print(f"🔑 Token: {HF_TOKEN[:10]}...{HF_TOKEN[-4:]}")
print("\nYou can now run:")
print("  python fetch_model_sizes.py")
print("  python retry_failed_models.py")
print("  python Downloader_Gradio_App.py")

if __name__ == "__main__":
    # Test token validity
    try:
        from huggingface_hub import HfApi
        api = HfApi(token=HF_TOKEN)
        user_info = api.whoami()
        print(f"\n✅ Token is valid! Logged in as: {user_info['name']}")
    except Exception as e:
        print(f"\n⚠️  Warning: Could not validate token: {e}")
        print("The token might still work for public repositories.") 