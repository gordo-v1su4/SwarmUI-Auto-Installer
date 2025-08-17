#!/usr/bin/env python3
"""
Random Init Image Helper for SwarmUI

This script randomly selects an image from a source folder and copies it
to a fixed filename that SwarmUI can use as an init image.

Usage:
1. Put your init images in SwarmUI/Data/Wildcards/random_images/
2. Set SwarmUI's Init Image to: SwarmUI/Data/Wildcards/current_random_init.png
3. Run this script before each generation (or set it up as a batch process)

The script will randomly pick an image and copy it to the fixed location.
"""

import os
import random
import shutil
import sys
from pathlib import Path

# Configuration - Using local folder structure
RANDOM_IMAGES_DIR = "random_init_images"
OUTPUT_IMAGE_PATH = "current_random_init.png"

# Alternative: If SwarmUI .gitignore allows, use this instead:
# RANDOM_IMAGES_DIR = "SwarmUI/Data/Wildcards/random_images"
# OUTPUT_IMAGE_PATH = "SwarmUI/Data/Wildcards/current_random_init.png"

# Supported image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}

def get_random_image():
    """Select a random image from the random_images directory."""
    
    if not os.path.exists(RANDOM_IMAGES_DIR):
        print(f"Error: Directory {RANDOM_IMAGES_DIR} does not exist!")
        print("Please create the directory and add some images to it.")
        return None
    
    # Get all image files from the directory
    image_files = []
    for file in os.listdir(RANDOM_IMAGES_DIR):
        if Path(file).suffix.lower() in IMAGE_EXTENSIONS:
            image_files.append(os.path.join(RANDOM_IMAGES_DIR, file))
    
    if not image_files:
        print(f"Error: No image files found in {RANDOM_IMAGES_DIR}")
        print(f"Supported formats: {', '.join(IMAGE_EXTENSIONS)}")
        return None
    
    # Randomly select an image
    selected_image = random.choice(image_files)
    print(f"Selected random image: {selected_image}")
    
    return selected_image

def copy_random_image():
    """Copy a randomly selected image to the output location."""
    
    selected_image = get_random_image()
    if selected_image is None:
        return False
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(OUTPUT_IMAGE_PATH), exist_ok=True)
        
        # Copy the selected image to the fixed output path
        shutil.copy2(selected_image, OUTPUT_IMAGE_PATH)
        print(f"Copied to: {OUTPUT_IMAGE_PATH}")
        
        return True
        
    except Exception as e:
        print(f"Error copying image: {e}")
        return False

def main():
    """Main function."""
    print("SwarmUI Random Init Image Helper")
    print("=" * 35)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        # List available images
        if not os.path.exists(RANDOM_IMAGES_DIR):
            print(f"Directory {RANDOM_IMAGES_DIR} does not exist!")
            return
            
        image_files = []
        for file in os.listdir(RANDOM_IMAGES_DIR):
            if Path(file).suffix.lower() in IMAGE_EXTENSIONS:
                image_files.append(file)
        
        if image_files:
            print(f"Available images in {RANDOM_IMAGES_DIR}:")
            for i, img in enumerate(image_files, 1):
                print(f"  {i}. {img}")
        else:
            print("No images found!")
        return
    
    # Copy a random image
    if copy_random_image():
        print("Success! Use the following path in SwarmUI's Init Image field:")
        print(f"  {OUTPUT_IMAGE_PATH}")
    else:
        print("Failed to copy random image.")

if __name__ == "__main__":
    main()
