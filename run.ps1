# SOJPE C2H Phase 1 - Complete Application Launcher
# Starts both dashboard frontend and Flask backend API

Write-Host "`n" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "SOJPE C2H - Phase 1 Automation Platform" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green

# Check Python installation
Write-Host "`n[CHECK] Python Installation..." -ForegroundColor Cyan
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python found: $pythonCheck" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Install Python 3.8+ and try again." -ForegroundColor Red
    exit 1
}

# Install dependencies
Write-Host "`n[SETUP] Installing Python dependencies..." -ForegroundColor Cyan
pip install -q -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ Dependency installation failed" -ForegroundColor Red
    exit 1
}

# Start HTTP server for frontend
Write-Host "`n[FRONTEND] Starting dashboard server (Port 8000)..." -ForegroundColor Cyan
$httpServer = Start-Process python -ArgumentList "-m http.server 8000" -WindowStyle Hidden -PassThru
Write-Host "✓ Dashboard available at: http://localhost:8000/dashboard.html" -ForegroundColor Green

# Start Flask backend
Write-Host "`n[BACKEND] Starting API server (Port 5000)..." -ForegroundColor Cyan
Start-Process python -ArgumentList "app.py" -WindowStyle Normal
Write-Host "✓ API available at: http://localhost:5000" -ForegroundColor Green

Write-Host "`n" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "SOJPE C2H Phase 1 - READY" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green

Write-Host "`nAccess Points:" -ForegroundColor Yellow
Write-Host "  Dashboard: http://localhost:8000/dashboard.html" -ForegroundColor White
Write-Host "  Upload:    http://localhost:8000/upload.html" -ForegroundColor White
Write-Host "  API:       http://localhost:5000/api" -ForegroundColor White

Write-Host "`nKeep this window open. Press Ctrl+C to stop all services." -ForegroundColor Gray

# Keep main process alive
while ($true) {
    Start-Sleep -Seconds 1
}
