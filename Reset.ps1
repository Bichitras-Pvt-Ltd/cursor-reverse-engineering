# Run as Administrator!
# --------------------------------------------
# ThinZin -
# todo -> add UI, auto mailing, sign up and auto logging (mail.tm garnu parla)
# --------------------------------------------

# Header
Clear-Host
Write-Host "`n=== Cursor Trial Reset Utility ===`n" -ForegroundColor Cyan
Write-Host "[*] Script started at $(Get-Date -Format 'HH:mm:ss')`n" -ForegroundColor Gray

# --------------------------------------------
# Part 1: Terminate Cursor Processes
# --------------------------------------------
Write-Host "[*] Terminating Cursor processes..." -ForegroundColor Gray
try {
    Get-Process "cursor" -ErrorAction Stop | Stop-Process -Force -ErrorAction Stop
    Write-Host "  [+] Success: All Cursor processes terminated`n" -ForegroundColor Green
} catch {
    Write-Host "  [!] Warning: No Cursor processes found (or already terminated)`n" -ForegroundColor Yellow
}

# --------------------------------------------
# Part 2: Delete Registry Keys
# --------------------------------------------
$regPaths = @(
    "HKCU:\Software\Cursor",
    "HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Compatibility Assistant\Store",
    "HKLM:\SOFTWARE\Microsoft\RADAR\HeapLeakDetection\DiagnosedApplications\Cursor.exe"
)

Write-Host "[*] Scanning registry keys..." -ForegroundColor Gray
$deletedRegKeys = @()

foreach ($path in $regPaths) {
    try {
        if (Test-Path $path) {
            Remove-Item -Path $path -Recurse -Force -ErrorAction Stop
            $deletedRegKeys += $path
            Write-Host "  [+] Deleted: $path" -ForegroundColor Green
        } else {
            Write-Host "  [ ] Not Found: $path" -ForegroundColor DarkGray
        }
    } catch {
        Write-Host "  [X] Failed to delete: $path (Error: $($_.Exception.Message))" -ForegroundColor Red
    }
}
Write-Host ""

# --------------------------------------------
# Part 3: Delete Files/Folders
# --------------------------------------------
$filePaths = @(
    "$env:AppData\Cursor",
    "$env:LocalAppData\cursor-updater",
    "$env:LocalAppData\Programs\cursor",
    "$env:Prefetch\CURSOR.EXE-*.pf",
    "$env:Prefetch\UNINSTALL CURSOR.EXE-*.pf"
)

Write-Host "[*] Scanning files/folders..." -ForegroundColor Gray
$deletedFiles = @()

foreach ($path in $filePaths) {
    try {
        $resolvedPaths = Resolve-Path $path -ErrorAction SilentlyContinue
        if ($resolvedPaths) {
            Remove-Item -Path $path -Recurse -Force -ErrorAction Stop
            $deletedFiles += $path
            Write-Host "  [+] Deleted: $path" -ForegroundColor Green
        } else {
            Write-Host "  [ ] Not Found: $path" -ForegroundColor DarkGray
        }
    } catch {
        Write-Host "  [X] Failed to delete: $path (Error: $($_.Exception.Message))" -ForegroundColor Red
    }
}
Write-Host ""

# --------------------------------------------
# Final Report
# --------------------------------------------
Write-Host "`n=== Results ===" -ForegroundColor Cyan
Write-Host "[+] Deleted $($deletedRegKeys.Count) registry keys" -ForegroundColor Green
Write-Host "[+] Deleted $($deletedFiles.Count) files/folders" -ForegroundColor Green

if ($deletedRegKeys.Count -gt 0 -or $deletedFiles.Count -gt 0) {
    Write-Host "`n=== Trial Successfully Reset! ===`n" -ForegroundColor Cyan -BackgroundColor DarkBlue
    Write-Host "  You can now launch Cursor and sign in with a new account.`n" -ForegroundColor White
} else {
    Write-Host "`n[!] No traces found. Cursor might already be clean.`n" -ForegroundColor Yellow
}

# Pause for visibility
Read-Host "Press Enter to exit..."