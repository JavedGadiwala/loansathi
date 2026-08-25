# LoanSathi Personal - Installation & Setup Guide

## Windows Installation

### System Requirements

- **Operating System:** Windows 10 or later (64-bit)
- **Python:** Python 3.12 or later (if running from source)
- **RAM:** Minimum 2 GB (4 GB recommended)
- **Disk Space:** 500 MB free space
- **No internet required** for core functionality

### Quick Start

#### Option 1: Using the Windows Batch Launcher (Recommended)

1. **Extract the LoanSathi folder** to your desired location (e.g., `C:\LoanSathi`)
2. **Double-click** `Start LoanSathi.bat`
   - First time: Will automatically install Python dependencies
   - Subsequent runs: Starts instantly
3. **Application opens** at `http://localhost:8501`
4. **To stop:** Close the command window or press Ctrl+C

#### Option 2: Using Python Command Line

```bash
cd C:\LoanSathi
pip install -r requirements.txt
streamlit run src/app.py
```

### First-Time Setup

When you first run LoanSathi, it will automatically:

1. Create local database (`data/global.db`)
2. Initialize configuration files in `data/config/`
3. Create folder structure for cases
4. Set default settings

**All data stays local on your computer.**

---

## Building Windows Executable

To create a standalone .exe file:

```bash
cd C:\LoanSathi
python build_windows_exe.py
```

This creates `dist\LoanSathi Personal.exe`

---

## Troubleshooting

### "Python is not installed" Error

Download and install Python 3.12+ from https://www.python.org/

During installation, check:
- Add Python to PATH
- Install for all users (if shared computer)

### "Port 8501 is already in use" Error

Run on a different port:
```bash
streamlit run src/app.py --server.port 8502
```

### Application Won't Start

Check the log file in the `logs/` folder for errors.

---

## Data Security

✅ All data stays on your computer
✅ No cloud upload
✅ No login required
✅ No tracking

---

**Version:** 0.1.0 (Phase 1 Complete)

**Status:** Ready for use
