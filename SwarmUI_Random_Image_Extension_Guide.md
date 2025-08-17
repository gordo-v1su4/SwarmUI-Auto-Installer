# SwarmUI Random Image Extension Guide

This guide covers the **Random Image Extension** - a proper SwarmUI extension that adds random image selection directly to the Generate tab interface, without overriding your normal workflow.

## 🎯 What This Extension Does

**Adds a "🎲 Random Image" button** directly to the Init Image section of SwarmUI's Generate tab, allowing you to:

- ✅ **One-click random image selection** from your collection
- ✅ **Perfect Generate Forever integration** - no manual scripts needed
- ✅ **Works with normal SwarmUI interface** - doesn't override anything
- ✅ **Configurable folder paths** via settings dialog
- ✅ **Visual feedback** and notifications
- ✅ **Combines perfectly with wildcards**

## 🚀 Installation & Setup

### Step 1: Restart SwarmUI
The extension is already installed in your SwarmUI fork. Simply **restart SwarmUI** to activate it.

### Step 2: Check Extensions Tab
1. Go to **Server** → **Extensions** in SwarmUI
2. You should see **"Random Image Extension"** in the installed extensions list
3. If not visible, check the SwarmUI console for any errors

## 📋 How to Use

### Basic Usage
1. **Open SwarmUI** and go to the **Generate** tab
2. **Expand the "Init Image" section** (click the toggle if collapsed)
3. **You'll see two new buttons**:
   - **🎲 Random Image** - Select a random image
   - **⚙️** - Settings dialog to configure folder path

### First Time Setup
1. **Click the ⚙️ settings button**
2. **Verify the folder path** (default: `random_init_images`)
3. **Make sure your images are in that folder**
4. **Click Save**

### Generate Forever Workflow
This is where the extension truly shines:

1. **Set up your prompt** with wildcards:
   ```
   {characters} in a {cinematic_look} style
   ```

2. **Click "🎲 Random Image"** to select initial random image

3. **Configure your other parameters** (creativity, etc.)

4. **Enable "Generate Forever"** in SwarmUI

5. **For each generation**:
   - SwarmUI generates with current random image
   - When you want a new image, click "🎲 Random Image" again
   - Continue generating with the new random image

## ⚙️ Configuration

### Folder Settings
- **Default folder**: `random_init_images` (in your project root)
- **Supported formats**: PNG, JPG, JPEG, BMP, TIFF, WEBP
- **Custom paths**: Use the ⚙️ settings button to change folder
- **Examples**:
  - `random_init_images` - Main collection
  - `portraits` - Specific category
  - `images/references` - Subfolder organization

### Folder Structure Example
```
SwarmUI_Model_Downloader/
├── random_init_images/           # Your random images
│   ├── portrait_01.jpg
│   ├── concept_02.png
│   ├── reference_03.jpg
│   └── style_04.webp
├── SwarmUI/
└── other files...
```

## 🎨 Perfect Combinations

### Maximum Variety Setup
```
Prompt: {characters} in a {cinematic_look} style
Init Image: [Click 🎲 Random Image button]
Init Image Creativity: 0.6
Generate Forever: ON
```

**Result**: Every generation gets:
- Random character from your text wildcards
- Random cinematic style from your text wildcards  
- Random reference image from your image collection
- **Infinite creative variety!**

### Organized Collections
Create subfolders for different types:
```
random_init_images/
├── portraits/
├── landscapes/ 
├── concepts/
└── styles/
```
Use settings to switch between: `random_init_images/portraits`, etc.

## 🔧 Features

### Smart Path Detection
The extension automatically searches for your folder in multiple locations:
- Direct path (if absolute)
- Relative to current directory
- Relative to SwarmUI root
- Up one directory level

### Visual Feedback
- **Button states**: Shows "⏳ Selecting..." while working
- **Success notifications**: "✅ Random image selected: filename.jpg"
- **Error notifications**: Clear error messages if something goes wrong
- **Toast notifications**: Auto-dismiss after 4 seconds

### API Integration
The extension provides an API at `/API/SelectRandomImageAPI` for:
- External automation scripts
- Integration with other tools
- Custom workflows

## 🐛 Troubleshooting

### Button Not Appearing
- **Check Init Image section is expanded** - click the section header
- **Restart SwarmUI** - extension needs a full restart to load
- **Check console** - look for JavaScript errors
- **Wait a few seconds** - button adds itself dynamically

### "Folder not found" Error
- **Check folder exists**: Verify `random_init_images` folder exists
- **Use settings dialog**: Click ⚙️ to configure correct path
- **Try absolute path**: Use full path like `D:/my_images` if needed

### "No images found" Error
- **Add images to folder**: Put JPG/PNG files in your folder
- **Check file extensions**: Must be png, jpg, jpeg, bmp, tiff, or webp
- **Check folder contents**: Use file explorer to verify images are there

### API Errors
- **Check SwarmUI logs**: Look for detailed error messages
- **Verify permissions**: Extension requires `randimg_use_random_image` permission
- **Restart SwarmUI**: Sometimes fixes API registration issues

## 🎯 Advanced Usage

### Batch Generation
1. Click "🎲 Random Image" for first image
2. Generate a batch (set Images = 4)
3. Click "🎲 Random Image" again for next batch
4. Repeat for variety

### Integration with Presets
- Save your favorite settings as SwarmUI presets
- Use Random Image with different presets
- Create preset collections for different styles

### Multiple Collections
- Create different folders for different themes
- Use settings to switch between them
- Organize by style, character type, etc.

## 💡 Tips & Best Practices

1. **Consistent aspect ratios**: Keep images similar sizes for better results
2. **Descriptive filenames**: Help track which images work best
3. **Organize by theme**: Use subfolders for different image types
4. **Backup favorites**: Keep copies of your best reference images
5. **Regular cleanup**: Remove images that don't work well

## 🔄 Compared to Other Methods

### ✅ Extension Benefits vs Python Scripts:
- **No external scripts** - built into SwarmUI
- **No command line needed** - click button in UI
- **Visual feedback** - see what's happening
- **Error handling** - clear error messages
- **Settings persistence** - remembers your folder

### ✅ Extension Benefits vs ComfyUI Workflows:
- **Keep normal SwarmUI interface** - no workflow override
- **All SwarmUI features available** - parameters, wildcards, etc.
- **Easy to use** - just click a button
- **No workflow complexity** - works with standard interface

This extension gives you the best of both worlds - powerful random image selection with the familiar SwarmUI interface! 🎉
