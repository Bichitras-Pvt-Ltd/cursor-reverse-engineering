# Cursor Almost done, 

## todo list:
- [ ] spilt screen
- [ ] human verfication
- [ ] reset and account gen mode

## Project Structure

```
cursor-trail-reset/
├── src/                    # Source code
│   ├── bot/               # Bot implementation
│   │   ├── __init__.py
│   │   ├── cursor_bot.py  # Main bot logic
│   │   └── mail_api.py    # Mail.tm API handling
│   └── gui/               # GUI implementation
│       └── cursor_gui.ps1 # PowerShell GUI script
├── data/                  # Data files
│   ├── accounts/         # Generated accounts
│   └── logs/            # Log files
├── config/               # Configuration files
│   └── settings.json    # Bot settings
├── scripts/             # Utility scripts
│   └── cleanup.ps1      # Cleanup script
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8 or higher
- Google Chrome browser
- PowerShell 7.0 or higher
- Windows 10/11

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cursor-trail-reset.git
cd cursor-trail-reset
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `config/settings.json` to customize:
- Default credentials (first name, last name, password)
- File paths for accounts and logs
- Browser settings (user agent, window size, timeout)

## Usage

### GUI Interface

Run the PowerShell GUI script:
```powershell
.\src\gui\cursor_gui.ps1
```

The GUI provides:
- Input fields for credentials
- "Generate Temp Mail" button to create accounts
- Output display area
- "Copy to Clipboard" button for easy copying

### Command Line

Run the bot directly:
```bash
python src/bot/cursor_bot.py
```

### Cleanup

To clean temporary files and reset the environment:
```powershell
.\scripts\cleanup.ps1
```

## Features

- Modern dark-themed GUI
- Automatic Cloudflare verification handling
- Account credentials saving
- Detailed logging
- Chrome profile management
- Easy cleanup utility

## Troubleshooting

1. If you encounter Cloudflare verification:
   - The script will pause and wait for manual verification
   - Complete the verification in the browser window
   - The script will continue automatically

2. If Chrome fails to start:
   - Run the cleanup script
   - Delete the chrome_profile directory
   - Try again

3. For any other issues:
   - Check the logs in `data/logs/debug.log`
   - Run the cleanup script
   - Ensure Chrome is up to date

 