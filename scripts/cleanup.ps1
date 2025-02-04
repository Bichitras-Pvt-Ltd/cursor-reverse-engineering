# Get the script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootPath = Split-Path -Parent $scriptPath

# Load settings
$settingsPath = Join-Path $rootPath "config\settings.json"
$settings = Get-Content $settingsPath | ConvertFrom-Json

# Define paths to clean
$pathsToClean = @(
    (Join-Path $rootPath $settings.paths.chrome_profile),
    (Join-Path $rootPath "data\logs"),
    (Join-Path $rootPath "__pycache__"),
    (Join-Path $rootPath "*.pyc"),
    (Join-Path $rootPath "*.pyo"),
    (Join-Path $rootPath "*.pyd"),
    (Join-Path $rootPath ".pytest_cache"),
    (Join-Path $rootPath "build"),
    (Join-Path $rootPath "dist"),
    (Join-Path $rootPath "*.egg-info")
)

Write-Host "Starting cleanup..." -ForegroundColor Yellow

foreach ($path in $pathsToClean) {
    if (Test-Path $path) {
        Write-Host "Removing $path..." -ForegroundColor Cyan
        Remove-Item -Path $path -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Create necessary directories
$dirsToCreate = @(
    (Split-Path -Parent (Join-Path $rootPath $settings.paths.accounts_file)),
    (Split-Path -Parent (Join-Path $rootPath $settings.paths.logs_file))
)

foreach ($dir in $dirsToCreate) {
    if (-not (Test-Path $dir)) {
        Write-Host "Creating directory $dir..." -ForegroundColor Green
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Host "Cleanup completed successfully!" -ForegroundColor Green 