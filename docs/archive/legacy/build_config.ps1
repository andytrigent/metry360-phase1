# Create SOJPE Config workbook with Named Ranges

Write-Host "Creating Config workbook..." -ForegroundColor Cyan

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false

$wb = $excel.Workbooks.Add()
$ws = $wb.ActiveSheet
$ws.Name = "Config"

# Header
$ws.Cells(1, 1) = "SOJPE C2H CONFIGURATION SHEET"
$ws.Cells(1, 1).Font.Size = 12
$ws.Cells(1, 1).Font.Bold = $true

# Canonical AM Table
$row = 3
$ws.Cells($row, 1) = "CANONICAL AMS (CanonicalAMTable)"
$ws.Cells($row, 1).Font.Bold = $true

$row = 4
$ws.Cells($row, 1) = "AM Name"
$ws.Cells($row, 2) = "AM ID"
$ws.Cells($row, 1).Font.Bold = $true
$ws.Cells($row, 2).Font.Bold = $true

$dataStart = 5
$ws.Cells($dataStart, 1) = "Priyanka Gadadmathad"; $ws.Cells($dataStart, 2) = 1001
$ws.Cells($dataStart + 1, 1) = "Tanu Gupta"; $ws.Cells($dataStart + 1, 2) = 1002
$ws.Cells($dataStart + 2, 1) = "Bharath C N"; $ws.Cells($dataStart + 2, 2) = 1003
$ws.Cells($dataStart + 3, 1) = "Anuradha H"; $ws.Cells($dataStart + 3, 2) = 1004
$ws.Cells($dataStart + 4, 1) = "Roshan Dominic"; $ws.Cells($dataStart + 4, 2) = 1005
$ws.Cells($dataStart + 5, 1) = "Bindu T S"; $ws.Cells($dataStart + 5, 2) = 1006
$ws.Cells($dataStart + 6, 1) = "Abhilash S"; $ws.Cells($dataStart + 6, 2) = 1007
$ws.Cells($dataStart + 7, 1) = "Kavita Nyamagoud"; $ws.Cells($dataStart + 7, 2) = 1008

# Config Parameters
$row = 14
$ws.Cells($row, 1) = "CONFIG PARAMETERS"
$ws.Cells($row, 1).Font.Bold = $true

$paramStart = 15
$ws.Cells($paramStart, 1) = "PurgeN"; $ws.Cells($paramStart, 2) = 5
$ws.Cells($paramStart + 1, 1) = "RetryMaxN"; $ws.Cells($paramStart + 1, 2) = 3
$ws.Cells($paramStart + 2, 1) = "WorkingDays"; $ws.Cells($paramStart + 2, 2) = 22
$ws.Cells($paramStart + 3, 1) = "MonthlyTargets"; $ws.Cells($paramStart + 3, 2) = 100

# Format
$ws.Columns.Item(1).ColumnWidth = 35
$ws.Columns.Item(2).ColumnWidth = 20

# Named Ranges
$wb.Names.Add("CanonicalAMTable") | Out-Null
$wb.Names.Item("CanonicalAMTable").RefersTo = "=Config!A5:B12"

$wb.Names.Add("PurgeN") | Out-Null
$wb.Names.Item("PurgeN").RefersTo = "=Config!B15"

$wb.Names.Add("RetryMaxN") | Out-Null
$wb.Names.Item("RetryMaxN").RefersTo = "=Config!B16"

$wb.Names.Add("WorkingDays") | Out-Null
$wb.Names.Item("WorkingDays").RefersTo = "=Config!B17"

$wb.Names.Add("MonthlyTargets") | Out-Null
$wb.Names.Item("MonthlyTargets").RefersTo = "=Config!B18"

$wb.Names.Add("ErrorsHeader") | Out-Null
$wb.Names.Item("ErrorsHeader").RefersTo = "=Config!A20:F20"

$wb.Names.Add("RagThresholds") | Out-Null
$wb.Names.Item("RagThresholds").RefersTo = "=Config!A22:B25"

# Save
$outputFile = "D:\experiments\gcc-qmetry\metry360-phase1\SOJPE_Config.xlsx"
$wb.SaveAs($outputFile, -4143)
$wb.Close()
$excel.Quit()

[System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null

Write-Host "[OK] Config workbook created" -ForegroundColor Green
Write-Host "[OK] 7 Named Ranges defined" -ForegroundColor Green

if (Test-Path $outputFile) {
    $size = (Get-Item $outputFile).Length / 1KB
    Write-Host ("[OK] File size: " + [math]::Round($size, 1) + " KB") -ForegroundColor Green
}
