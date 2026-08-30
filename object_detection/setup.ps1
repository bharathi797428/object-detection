cd c:\object_detection
Write-Host "Downloading YOLO files..."
$ProgressPreference = 'SilentlyContinue'

Write-Host "Downloading yolov3.weights (~236MB, this will take a few minutes)..."
Invoke-WebRequest -Uri "https://pjreddie.com/media/files/yolov3.weights" -OutFile "yolov3.weights" -UseBasicParsing

Write-Host "Downloading yolov3.cfg..."
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg" -OutFile "yolov3.cfg" -UseBasicParsing

Write-Host "Downloading coco.names..."
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names" -OutFile "coco.names" -UseBasicParsing

Write-Host "Download complete!"
Write-Host "Files downloaded:"
Get-Item *.weights, *.cfg, *.names | ForEach-Object { Write-Host "  - $($_.Name) ($([Math]::Round($_.Length/1MB, 2)) MB)" }
