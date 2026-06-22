# Create SOJPE Config workbook with Named Ranges
# PowerShell-native approach using COM

param([string]$OutputPath = ".\SOJPE_Config.xlsx")

Write-Host "Creating Config workbook..." -ForegroundColor Cyan

try {
    # Create Excel instance
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false

    # Create new workbook
    $wb = $excel.Workbooks.Add()
    $ws = $wb.ActiveSheet
    $ws.Name = "Config"

    # Header
    $ws.Cells.Item(1, 1).Value = "SOJPE C2H CONFIGURATION SHEET"
    $ws.Cells.Item(1, 1).Font.Size = 14
    $ws.Cells.Item(1, 1).Font.Bold = $true
    $ws.Range("A1:D1").Merge() | Out-Null

    # Section 1: Canonical AM Table
    $row = 3
    $ws.Cells.Item($row, 1).Value = "SECTION 1: CANONICAL AM NAME → ID MAPPING"
    $ws.Cells.Item($row, 1).Font.Bold = $true
    $ws.Range("A$row`:B$row").Merge() | Out-Null

    $row = 4
    $ws.Cells.Item($row, 1).Value = "AM Name"
    $ws.Cells.Item($row, 2).Value = "AM ID"
    $ws.Cells.Item($row, 1).Font.Bold = $true
    $ws.Cells.Item($row, 2).Font.Bold = $true

    # Sample AMs
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
        $ws.Cells.Item($dataStart + $i, 1).Value = $ams[$i][0]
        $ws.Cells.Item($dataStart + $i, 2).Value = $ams[$i][1]
    }

    # Define Named Range: CanonicalAMTable
    $canonicalRange = "Config!`$A`$$dataStart`:`$B`$($dataStart + $ams.Count - 1)"
    $wb.Names.Add("CanonicalAMTable") | Out-Null
    $wb.Names.Item("CanonicalAMTable").RefersTo = "=$canonicalRange"

    # Section 2: Config Parameters
    $row = $dataStart + $ams.Count + 2
    $ws.Cells.Item($row, 1).Value = "SECTION 2: CONFIGURATION PARAMETERS"
    $ws.Cells.Item($row, 1).Font.Bold = $true
    $ws.Range("A$row`:B$row").Merge() | Out-Null

    $paramStart = $row + 1
    $params = @(
        @("PurgeN (keep last N runs)", 5),
        @("RetryMaxN (max retries)", 3),
        @("WorkingDays (days in month)", 22),
        @("MonthlyTargets (base target)", 100)
    )

    foreach ($i in 0..($params.Count - 1)) {
        $ws.Cells.Item($paramStart + $i, 1).Value = $params[$i][0]
        $ws.Cells.Item($paramStart + $i, 2).Value = $params[$i][1]
    }

    # Define Named Ranges
    @("PurgeN", "RetryMaxN", "WorkingDays", "MonthlyTargets") | ForEach-Object {
        $wb.Names.Add($_) | Out-Null
    }

    $wb.Names.Item("PurgeN").RefersTo = "=Config!`$B`$$paramStart"
    $wb.Names.Item("RetryMaxN").RefersTo = "=Config!`$B`$($paramStart + 1)"
    $wb.Names.Item("WorkingDays").RefersTo = "=Config!`$B`$($paramStart + 2)"
    $wb.Names.Item("MonthlyTargets").RefersTo = "=Config!`$B`$($paramStart + 3)"

    # Section 3: Errors Tab Header
    $row = $paramStart + $params.Count + 2
    $ws.Cells.Item($row, 1).Value = "SECTION 3: ERRORS TAB SCHEMA"
    $ws.Cells.Item($row, 1).Font.Bold = $true
    $ws.Range("A$row`:F$row").Merge() | Out-Null

    $errorHeaderRow = $row + 1
    $errorCols = @("Raw Name", "Canonical Suggestion", "Confidence", "Source File", "Step #", "Timestamp")
    foreach ($i in 0..($errorCols.Count - 1)) {
        $ws.Cells.Item($errorHeaderRow, $i + 1).Value = $errorCols[$i]
        $ws.Cells.Item($errorHeaderRow, $i + 1).Font.Bold = $true
    }

    # Define ErrorsHeader Named Range
    $wb.Names.Add("ErrorsHeader") | Out-Null
    $wb.Names.Item("ErrorsHeader").RefersTo = "=Config!`$A`$$errorHeaderRow`:`$F`$$errorHeaderRow"

    # Add RagThresholds Named Range
    $wb.Names.Add("RagThresholds") | Out-Null
    $wb.Names.Item("RagThresholds").RefersTo = "=Config!`$A`$($errorHeaderRow + 2)`:`$B`$($errorHeaderRow + 5)"

    # Format columns
    $ws.Columns.Item(1).ColumnWidth = 35
    $ws.Columns.Item(2).ColumnWidth = 25
    $ws.Columns.Item(3).ColumnWidth = 20

    # Create Errors sheet (demo)
    $errorsSheet = $wb.Sheets.Add([Type]::Missing, [Type]::Missing, 1)
    $errorsSheet.Name = "Errors"
    foreach ($i in 0..($errorCols.Count - 1)) {
        $errorsSheet.Cells.Item(1, $i + 1).Value = $errorCols[$i]
        $errorsSheet.Cells.Item(1, $i + 1).Font.Bold = $true
    }

    # Save workbook
    $fullPath = (Resolve-Path -Path (Split-Path -Parent $OutputPath) -ErrorAction SilentlyContinue) + "\" + (Split-Path -Leaf $OutputPath)
    if (-not (Test-Path (Split-Path -Parent $OutputPath))) {
        mkdir (Split-Path -Parent $OutputPath) -Force | Out-Null
    }

    $wb.SaveAs($OutputPath)
    Write-Host "✓ Config workbook created: $OutputPath" -ForegroundColor Green
    Write-Host "✓ Named Ranges defined: CanonicalAMTable, PurgeN, RetryMaxN, WorkingDays, MonthlyTargets, ErrorsHeader, RagThresholds" -ForegroundColor Green

    # Close
    $wb.Close($false)
    $excel.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
}
catch {
    Write-Host "Error creating workbook: $_" -ForegroundColor Red
    exit 1
}
