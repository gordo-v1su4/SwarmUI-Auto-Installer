# Random Init Images for SwarmUI

This guide shows you how to use random images for initialization with each prompt generation in SwarmUI, similar to how wildcards work for text prompts.

## Overview

Unlike text wildcards (like `{characters}` or `{styles}`), SwarmUI doesn't have built-in support for image wildcards. However, we can achieve similar functionality using a combination of:

1. **A dedicated folder for random images**
2. **A Python script that randomly selects images**
3. **A fixed filename that SwarmUI always uses**

## Setup Instructions

### Step 1: Prepare Your Random Images

1. **The directory is already created**:
   ```
   random_init_images/
   ```

2. **Add your init images** to this folder:
   - Copy all the images you want to randomly select from
   - Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`
   - Name them descriptively (e.g., `concept_art_01.jpg`, `reference_02.png`)

### Step 2: Configure SwarmUI

1. **In SwarmUI's Init Image field**, use this **fixed path** (relative to your project folder):
   ```
   current_random_init.png
   ```

2. **Set your Init Image Creativity** as desired (e.g., 0.6)

3. **Enable the Init Image group** by checking the toggle

### Step 3: Use the Random Image Script

Run the script before each generation (or batch of generations):

```bash
# Windows
python random_init_image.py

# Linux/Mac  
python3 random_init_image.py
```

The script will:
- Randomly select an image from `random_images/` folder
- Copy it to `current_random_init.png`
- Display which image was selected

## Usage Examples

### Basic Usage
```bash
python random_init_image.py
```
Output:
```
SwarmUI Random Init Image Helper
===================================
Selected random image: random_init_images/concept_art_03.jpg
Copied to: current_random_init.png
Success! Use the following path in SwarmUI's Init Image field:
  current_random_init.png
```

### List Available Images
```bash
python random_init_image.py --list
```

### Batch Generation Workflow

1. **Set up your prompt with text wildcards**:
   ```
   {characters} in a {cinematic_look} style
   ```

2. **Configure init image**:
   - Init Image: `current_random_init.png`
   - Init Image Creativity: `0.6`

3. **Generate multiple images**:
   ```bash
   # Get a new random image
   python random_init_image.py
   
   # Generate in SwarmUI (set Images = 4)
   # Repeat as desired
   ```

## Advanced Usage

### Integration with Batch Scripts

Create a batch script for Windows (`generate_batch.bat`):
```batch
@echo off
for /l %%i in (1,1,10) do (
    echo Generating batch %%i...
    python random_init_image.py
    timeout /t 2 /nobreak >nul
    echo Run your SwarmUI generation now, then press any key to continue...
    pause >nul
)
```

### API Integration

If you use SwarmUI's API, you can automate the entire process:
```python
import requests
import subprocess

# Select random image
subprocess.run(["python", "random_init_image.py"])

# Make API call to SwarmUI
api_data = {
    "prompt": "a beautiful landscape",
    "initimage": "current_random_init.png",
    "initimagecreativity": 0.6
}
response = requests.post("http://localhost:7801/API/GenerateText2Image", json=api_data)
```

## Troubleshooting

### "Directory does not exist" Error
- Make sure the `random_init_images/` directory exists in your project folder
- Check that you're running the script from the correct directory

### "No image files found" Error  
- Add image files to the `random_init_images/` folder
- Ensure files have supported extensions: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.webp`

### SwarmUI can't find init image
- Verify the path in SwarmUI exactly matches: `current_random_init.png`
- Make sure you ran the random script at least once to create the file

## File Structure

Your final structure should look like:
```
SwarmUI_Model_Downloader/
├── SwarmUI/
│   └── Data/
│       └── Wildcards/
│           ├── Carlos.txt              # Your text wildcards
│           ├── Characters.txt
│           └── ...
├── random_init_images/                # Your source images
│   ├── concept_art_01.jpg
│   ├── reference_02.png
│   └── style_03.jpg
├── current_random_init.png            # Current selected image (created by script)
├── random_init_image.py               # The helper script
└── Random_Init_Images_Guide.md        # This guide
```

## Tips

1. **Organize your images** by type in subfolders, then run the script from different folders
2. **Use consistent aspect ratios** for better results
3. **Combine with text wildcards** for maximum variety
4. **Test different creativity values** (0.4-0.8) to find what works best
5. **Keep backups** of your favorite init images
