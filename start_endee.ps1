# PowerShell script to start the Endee Database in WSL
# This ensures it uses the correct internal data directory

Write-Host "Starting Endee Vector Database in WSL..." -ForegroundColor Cyan

# Check if WSL is available
if (!(Get-Command wsl -ErrorAction SilentlyContinue)) {
    Write-Error "WSL is not installed. Please install WSL to run Endee."
    exit 1
}

# Start Endee inside WSL as root using the internal data directory
wsl -u root bash -c "cd /mnt/c/Users/roysa/OneDrive/Desktop/endeeproject-master && NDD_DATA_DIR=/root/endee-data ./build/ndd-avx2"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Endee Database started successfully on http://localhost:8080" -ForegroundColor Green
} else {
    Write-Error "Failed to start Endee Database."
}
