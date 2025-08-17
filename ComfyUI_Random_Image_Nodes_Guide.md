# ComfyUI Random Image Nodes for SwarmUI

This guide shows you how to use the new **SwarmRandomImageLoader** and **SwarmRandomImagePath** nodes in SwarmUI's ComfyUI backend for automatic random image selection.

## 🎯 What This Solves

Instead of manually running Python scripts, these ComfyUI nodes automatically select random images **within the workflow itself**. Perfect for:

- **Generate Forever** mode with different images each time
- **Batch generation** with automatic variety
- **Integration with wildcards** and other ComfyUI nodes
- **Seamless workflow automation**

## 🔧 Installation

The nodes are automatically available after committing the changes to your SwarmUI fork. Simply restart SwarmUI to load the new nodes.

## 📝 Available Nodes

### 1. Random Image Loader
- **Node Name**: `SwarmRandomImageLoader`
- **Category**: `SwarmUI/images`
- **Purpose**: Directly loads a random image and returns it as an IMAGE tensor

**Inputs:**
- `folder_path` (STRING): Path to your images folder (default: "random_init_images")
- `seed` (INT): Seed for random selection (use -1 for truly random)
- `image_extensions` (STRING): Allowed file types (default: "png,jpg,jpeg,bmp,tiff,webp")

**Outputs:**
- `image` (IMAGE): The loaded random image
- `filename` (STRING): The filename of the selected image

### 2. Random Image Path
- **Node Name**: `SwarmRandomImagePath` 
- **Category**: `SwarmUI/images`
- **Purpose**: Returns a random image path for use with other nodes

**Inputs:**
- `folder_path` (STRING): Path to your images folder
- `seed` (INT): Seed for random selection 
- `image_extensions` (STRING): Allowed file types

**Outputs:**
- `image_path` (STRING): Full path to the selected random image

## 🚀 Usage Examples

### Example 1: Basic Random Init Image

**Workflow:**
```
SwarmRandomImageLoader → Load Image (init) → KSampler
```

**Setup:**
1. Add `SwarmRandomImageLoader` node
2. Set `folder_path` to your images folder
3. Connect the `image` output to your img2img workflow
4. Use seed from your main generation or set to -1 for random

### Example 2: Using with Generate Forever

**Workflow:**
```
SwarmRandomImageLoader → Your normal img2img workflow
    ↓ (seed connected to main seed)
```

**Benefits:**
- Each generation automatically gets a new random image
- Seed synchronization ensures reproducible results
- Works perfectly with SwarmUI's "Generate Forever" feature

### Example 3: Combined with Text Wildcards

**Workflow:**
```
SwarmRandomImageLoader → Load Image (init)
                           ↓
Text Wildcards → CLIP Text Encode → KSampler
```

**Result:**
- Random text prompts from your wildcards
- Random init images from your collection
- Maximum variety in every generation!

## 🎨 Advanced Workflows

### Seed-Synchronized Random Selection
```
Seed Input (123) → SwarmRandomImageLoader
     ↓               ↓
   KSampler ←── Load Image (init)
```
The same seed gives the same random image selection and generation.

### Multiple Random Sources
```
SwarmRandomImageLoader (folder: "portraits") → Load Image
SwarmRandomImageLoader (folder: "backgrounds") → Load Image  
     ↓                                               ↓
   Blend Images ←────────────────────────────────────┘
```

### Path-Based Workflow with Custom Processing
```
SwarmRandomImagePath → Custom Image Processing → Load Image → KSampler
```

## ⚙️ Configuration

### Folder Structure
Your images should be organized like:
```
SwarmUI_Model_Downloader/
├── random_init_images/           # Main folder
│   ├── portraits/               # Optional subfolders
│   ├── landscapes/
│   └── concepts/
```

### Folder Path Options
The nodes automatically search in multiple locations:
1. Direct path (if absolute)
2. Relative to ComfyUI base
3. Relative to SwarmUI root (recommended)
4. Up two directory levels

**Recommended paths:**
- `"random_init_images"` - Your main collection
- `"random_init_images/portraits"` - Specific category
- `"../some_folder"` - Custom location

### Seed Behavior
- **Fixed seed (e.g., 123)**: Same image selection every time
- **-1**: Truly random selection each time
- **Connected to main seed**: Changes with your generation seed

## 🔄 Integration with SwarmUI Features

### Generate Forever
1. Set up your workflow with `SwarmRandomImageLoader`
2. Enable "Generate Forever" in SwarmUI
3. Each generation automatically uses a different random image

### Wildcards Integration
- Use text wildcards in prompts: `{characters} in a {style}`
- Use random images for init: `SwarmRandomImageLoader`
- Result: Maximum creative variety!

### Batch Generation
- Set seed to -1 for different images per batch
- Or use incremental seeds for reproducible sequences

## 🐛 Troubleshooting

### "Could not find folder" Error
- Check that your `random_init_images` folder exists
- Verify the path in the `folder_path` input
- Try absolute paths if relative paths don't work

### "No image files found" Error
- Add images to your folder
- Check the `image_extensions` parameter
- Ensure file extensions match the allowed list

### Node Not Appearing
- Restart SwarmUI completely
- Check that the files were saved correctly
- Look for errors in the ComfyUI console

## 🎯 Tips and Best Practices

1. **Organize by Theme**: Use subfolders for different image types
2. **Consistent Aspect Ratios**: Keep images similar sizes for better results
3. **Seed Management**: Use -1 for variety, fixed seeds for consistency
4. **File Naming**: Use descriptive names for easier debugging
5. **Performance**: Large image collections are fine, selection is fast

## 🔮 Advanced Use Cases

### Dynamic Collections
Change the `folder_path` dynamically based on other workflow conditions.

### Metadata Integration
Use the `filename` output to track which images work best.

### Multi-Stage Random Selection
Chain multiple random selectors for complex scenarios.

This integration makes random image selection as easy as using wildcards for text! 🎉
