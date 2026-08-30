# Download YOLO files for object detection

$workspacePath = "c:\object_detection"
Set-Location $workspacePath

Write-Host "Downloading YOLO files..."
Write-Host "This may take several minutes due to the large weights file (~236MB)`n"

# Download yolov3.weights
Write-Host "1. Downloading yolov3.weights (this is a large file, please be patient)..."
try {
    $ProgressPreference = 'SilentlyContinue'
    Invoke-WebRequest -Uri "https://pjreddie.com/media/files/yolov3.weights" -OutFile "yolov3.weights" -ErrorAction Stop
    Write-Host "   ✓ yolov3.weights downloaded successfully"
}
catch {
    Write-Host "   ✗ Failed to download yolov3.weights: $_"
}

# Download yolov3.cfg
Write-Host "2. Downloading yolov3.cfg..."
try {
    # Remove corrupted file if it exists
    if (Test-Path "yolov3.cfg") {
        Remove-Item "yolov3.cfg" -Force
    }
    $Uri = "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg"
    Invoke-WebRequest -Uri $Uri -OutFile "yolov3.cfg" -ErrorAction Stop -UseBasicParsing
    Write-Host "   ✓ yolov3.cfg downloaded successfully"
}
catch {
    Write-Host "   ✗ Failed to download yolov3.cfg: $_"
}

# Download coco.names
Write-Host "3. Downloading coco.names..."
try {
    # Remove corrupted file if it exists
    if (Test-Path "coco.names") {
        Remove-Item "coco.names" -Force
    }
    $Uri = "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names"
    Invoke-WebRequest -Uri $Uri -OutFile "coco.names" -ErrorAction Stop -UseBasicParsing
    Write-Host "   ✓ coco.names downloaded successfully"
}
catch {
    Write-Host "   ✗ Failed to download coco.names: $_"
}

# Verify files
Write-Host "`nVerifying downloaded files..."
$files = @("yolov3.weights", "yolov3.cfg", "coco.names")
$allExist = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        $size = (Get-Item $file).Length / 1MB
        Write-Host "✓ $file exists ($('{0:F2}' -f $size) MB)"
    } else {
        Write-Host "✗ $file is missing"
        $allExist = $false
    }
}

if ($allExist) {
    Write-Host "`n✓ All YOLO files downloaded successfully! You can now run: python model.py"
} else {
    Write-Host "`n✗ Some files failed to download. Please check your internet connection and try again."
}
