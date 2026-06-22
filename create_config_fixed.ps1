# Create SOJPE Config workbook with Named Ranges

Write-Host "Creating Config workbook..." -ForegroundColor Cyan

try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false

    $wb = $excel.Workbooks.Add()
    $ws = $wb.ActiveSheet
    $ws.Name = "Config"

    # Header
    $ws.Cells(1, 1) = "SOJPE C2H CONFIGURATION SHEET - DEMO"
    $ws.Cells(1, 1).Font.Size = 12
    $ws.Cells(1, 1).Font.Bold = $true

    # Canonical AM Table (Named Range: CanonicalAMTable)
    $row = 3
    $ws.Cells($row, 1) = "CANONICAL AMS (Named Range: CanonicalAMTable)"
    $ws.Cells($row, 1).Font.Bold = $true

    $row = 4
    $ws.Cells($row, 1) = "AM Name"
    $ws.Cells($row, 2) = "AM ID"
    $ws.Cells($row, 1).Font.Bold = $true
    $ws.Cells($row, 2).Font.Bold = $true

    $ams = @(
        @("Priyanka Gadadmathad", 1001),
        @("Tanu Gupta", 1002),
        @("Bharath C N", 1003),
        @("Anuradha H", 1004),
        @("Roshan Dominic", 1005),
        @("Bindu T S", 1006),
        @("Abhilash S", 1007),
        @("Kavita Nyamagoud", 1008)
    )

    $dataStart = 5
    foreach ($i in 0..($ams.Count - 1)) {
        $ws.Cells($dataStart + $i, 1) = $ams[$i][0]
        $ws.Cells($dataStart + $i, 2) = $ams[$i][1]
    }

    # Config Parameters Section
    $row = $dataStart + $ams.Count + 2
    $ws.Cells($row, 1) = "CONFIG PARAMETERS"
    $ws.Cells($row, 1).Font.Bold = $true

    $paramStart = $row + 1
    $ws.Cells($paramStart, 1) = "PurgeN (keep last N runs)"
    $ws.Cells($paramStart, 2) = 5

    $ws.Cells($paramStart + 1, 1) = "RetryMaxN (max retries)"
    $ws.Cells($paramStart + 1, 2) = 3

    $ws.Cells($paramStart + 2, 1) = "WorkingDays (days in month)"
    $ws.Cells($paramStart + 2, 2) = 22

    $ws.Cells($paramStart + 3, 1) = "MonthlyTargets (base target)"
    $ws.Cells($paramStart + 3, 2) = 100

    # Add Named Ranges
    $canonicalRange = "Config!`$A`$$dataStart`:`$B`$($dataStart + $ams.Count - 1)"
    $wb.Names.Add("CanonicalAMTable") | Out-Null
    $wb.Names.Item("CanonicalAMTable").RefersTo = "=$canonicalRange"

    $wb.Names.Add("PurgeN") | Out-Null
    $wb.Names.Item("PurgeN").RefersTo = "=Config!`$B`$$paramStart"

    $wb.Names.Add("RetryMaxN") | Out-Null
    $wb.Names.Item("RetryMaxN").RefersTo = "=Config!`$B`$($paramStart + 1)"

    $wb.Names.Add("WorkingDays") | Out-Null
    $wb.Names.Item("WorkingDays").RefersTo = "=Config!`$B`$($paramStart + 2)"

    $wb.Names.Add("MonthlyTargets") | Out-Null
    $wb.Names.Item("MonthlyTargets").RefersTo = "=Config!`$B`$($paramStart + 3)"

    # Errors Tab Header
    $row = $paramStart + 4 + 2
    $ws.Cells($row, 1) = "ERRORS TAB HEADER (ErrorsHeader Named Range)"
    $ws.Cells($row, 1).Font.Bold = $true

    $errorHeaderRow = $row + 1
    $errorCols = @("Raw Name", "Canonical Suggestion", "Confidence", "Source File", "Step #", "Timestamp")
    foreach ($i in 0..($errorCols.Count - 1)) {
        $ws.Cells($errorHeaderRow, $i + 1) = $errorCols[$i]
        $ws.Cells($errorHeaderRow, $i + 1).Font.Bold = $true
    }

    $errorRange = "Config!`$A`$$errorHeaderRow`:`$F`$$errorHeaderRow"
    $wb.Names.Add("ErrorsHeader") | Out-Null
    $wb.Names.Item("ErrorsHeader").RefersTo = "=$errorRange"

    # RAG Thresholds
    $wb.Names.Add("RagThresholds") | Out-Null
    $wb.Names.Item("RagThresholds").RefersTo = "=Config!`$A`$($errorHeaderRow + 2)`:`$B`$($errorHeaderRow + 5)"

    # Format columns
    $ws.Columns.Item(1).ColumnWidth = 35
    $ws.Columns.Item(2).ColumnWidth = 20

    # Save
    $outputFile = "D:\experiments\gcc-qmetry\metry360-phase1\SOJPE_Config.xlsx"
    $wb.SaveAs($outputFile, -4143)  # -4143 = Excel format
    $wb.Close()
    $excel.Quit()

    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
    Remove-Variable excel

    Write-Host "✓ Config workbook saved: $outputFile" -ForegroundColor Green
    Write-Host "✓ Named Ranges: CanonicalAMTable, PurgeN, RetryMaxN, WorkingDays, MonthlyTargets, ErrorsHeader, RagThresholds" -ForegroundColor Green

    # Verify file exists
    if (Test-Path $outputFile) {
        $size = (Get-Item $outputFile).Length / 1KB
        Write-Host "✓ File size: $([math]::Round($size, 1)) KB" -ForegroundColor Green
    }
}
catch {
    Write-Host ("Error: " + $_) -ForegroundColor Red
    exit 1
}
