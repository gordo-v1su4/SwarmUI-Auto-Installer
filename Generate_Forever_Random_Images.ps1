# Generate Forever with Random Images - PowerShell Script
# This script continuously generates new random images for SwarmUI

param(
    [int]$Count = 100,           # Number of generations to run
    [int]$DelaySeconds = 2,      # Delay between generations
    [string]$SwarmUIUrl = "http://localhost:7801",  # SwarmUI API URL
    [switch]$TestMode = $false   # Test mode - just shows what would happen
)

Write-Host "SwarmUI Generate Forever with Random Images" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green
Write-Host "Count: $Count generations" -ForegroundColor Cyan
Write-Host "Delay: $DelaySeconds seconds between generations" -ForegroundColor Cyan
Write-Host "SwarmUI URL: $SwarmUIUrl" -ForegroundColor Cyan
Write-Host "Test Mode: $($TestMode ? 'ON' : 'OFF')" -ForegroundColor Cyan
Write-Host ""

# Check if random image script exists
if (-not (Test-Path "random_init_image.py")) {
    Write-Host "ERROR: random_init_image.py not found in current directory!" -ForegroundColor Red
    Write-Host "Please run this script from the SwarmUI_Model_Downloader directory." -ForegroundColor Red
    exit 1
}

# Check if random images directory exists and has images
if (-not (Test-Path "random_init_images")) {
    Write-Host "ERROR: random_init_images directory not found!" -ForegroundColor Red
    exit 1
}

$imageFiles = Get-ChildItem "random_init_images" -Filter "*.png", "*.jpg", "*.jpeg", "*.bmp", "*.tiff", "*.webp" -ErrorAction SilentlyContinue
if ($imageFiles.Count -eq 0) {
    Write-Host "ERROR: No images found in random_init_images directory!" -ForegroundColor Red
    exit 1
}

Write-Host "Found $($imageFiles.Count) random images available" -ForegroundColor Green
Write-Host ""

# Main generation loop
for ($i = 1; $i -le $Count; $i++) {
    Write-Host "Generation $i of $Count" -ForegroundColor Yellow
    Write-Host "-" * 30 -ForegroundColor Yellow
    
    # Step 1: Select random image
    Write-Host "Selecting random image..." -ForegroundColor Cyan
    if ($TestMode) {
        Write-Host "[TEST MODE] Would run: python random_init_image.py" -ForegroundColor Magenta
    } else {
        $result = & python random_init_image.py
        Write-Host $result -ForegroundColor White
    }
    
    # Step 2: Wait for manual generation or API call
    if ($TestMode) {
        Write-Host "[TEST MODE] Would trigger SwarmUI generation" -ForegroundColor Magenta
    } else {
        Write-Host "Random image ready! Now run your generation in SwarmUI..." -ForegroundColor Green
        Write-Host "Press SPACE to continue to next random image, or 'Q' to quit" -ForegroundColor Yellow
        
        do {
            $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            if ($key.Character -eq 'q' -or $key.Character -eq 'Q') {
                Write-Host "`nStopping generation loop..." -ForegroundColor Red
                exit 0
            }
        } while ($key.Character -ne ' ')
    }
    
    Write-Host ""
    
    # Add delay if not the last iteration
    if ($i -lt $Count -and $DelaySeconds -gt 0) {
        Write-Host "Waiting $DelaySeconds seconds..." -ForegroundColor Gray
        Start-Sleep -Seconds $DelaySeconds
    }
}

Write-Host "Completed $Count generations!" -ForegroundColor Green
