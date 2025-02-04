# Cursor Trail Reset


## Prerequisites

- Python 3.7+
- Chrome browser installed
- PowerShell 5.1+ (for GUI)
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Method (Recommended)
1. Run the PowerShell GUI:
```powershell
.\cursor_mail_gui.ps1
```

2. The GUI provides:
   - Input fields for customization
   - One-click account generation
   - Real-time progress display
   - Easy credential copying

### Command Line Method
Run the Python script directly:
```bash
python cursor_bot.py
```

## Files Description

- `cursor_bot.py` - Main Python script for account creation
- `cursor_mail_gui.ps1` - PowerShell GUI interface
- `requirements.txt` - Python dependencies
- `cursor_accounts.txt` - Generated accounts (auto-created)

## Generated Files

The tool will create several files during operation:
- `cursor_accounts.txt` - Stores account credentials
- `debug_log.txt` - Debug information if errors occur
- `error_screenshot.png` - Screenshot if errors occur
- `chrome_profile/` - Chrome profile directory

## Notes

- All generated credentials are saved in `cursor_accounts.txt`
- The tool creates a new Chrome profile for each session
- Debug logs are available in `debug_log.txt` if errors occur
- This tool is for educational purposes only

## Troubleshooting

1. If you encounter Cloudflare verification:
   - The script will pause and wait for manual verification
   - Complete the verification in the browser window
   - The script will continue automatically

2. If Chrome fails to start:
   - Delete the `chrome_profile` directory
   - Restart the script

3. If account creation fails:
   - Check the debug log for details
   - Ensure Chrome is up to date
   - Try running the script again

## Security

- Generated credentials are stored locally
- Chrome profiles are isolated
- No data is sent to external servers except Mail.tm and Cursor

## Legal

This tool is for educational purposes only. Please ensure you comply with Cursor's terms of service when using automated tools. 