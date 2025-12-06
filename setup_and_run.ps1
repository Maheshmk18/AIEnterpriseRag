# Check for Python
if (-not (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

# Check for Node.js
if (-not (Get-Command "npm" -ErrorAction SilentlyContinue)) {
    Write-Host "Node.js (npm) is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "Installing Backend Dependencies..." -ForegroundColor Green
cd backend
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install backend dependencies." -ForegroundColor Red
    exit 1
}
cd ..

Write-Host "Installing Frontend Dependencies..." -ForegroundColor Green
cd frontend
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to install frontend dependencies." -ForegroundColor Red
    exit 1
}
cd ..

Write-Host "Starting Backend and Frontend..." -ForegroundColor Green

# Start Backend in background
$backendProcess = Start-Process -FilePath "python" -ArgumentList "-m uvicorn app.main:app --host 0.0.0.0 --port 8000" -WorkingDirectory "backend" -PassThru -NoNewWindow

# Start Frontend in background
$frontendProcess = Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory "frontend" -PassThru -NoNewWindow

Write-Host "Services started. Press Ctrl+C to stop." -ForegroundColor Yellow

try {
    # Wait for processes to exit
    Wait-Process -Id $backendProcess.Id, $frontendProcess.Id
}
catch {
    Stop-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue
    Stop-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue
}
