# Start Zenith Backend Server

Write-Host "Starting Zenith Mock Interview Backend Server..." -ForegroundColor Green

# Activate virtual environment
.\venv_new\Scripts\Activate.ps1

# Start server
Write-Host "Server starting at http://localhost:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

uvicorn api_main:app --host 0.0.0.0 --port 8000 --reload
