# Virtual Environment Guide

This project uses a Python virtual environment (`.venv`) to isolate dependencies.

## Why Use a Virtual Environment?

- **Dependency Isolation**: Keeps project dependencies separate from system Python
- **Version Control**: Ensures everyone uses the same package versions
- **Clean Development**: No conflicts with other Python projects
- **Easy Cleanup**: Just delete `.venv` folder to start fresh

## Quick Commands

### Activating the Virtual Environment

**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows (cmd):**
```cmd
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

You'll know it's active when you see `(.venv)` at the start of your terminal prompt.

### Deactivating

```bash
deactivate
```

### Installing New Packages

With the virtual environment active:
```bash
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt
```

### Checking Active Python

```bash
which python  # macOS/Linux
where python  # Windows
```

Should point to `.venv/bin/python` (or `.venv\Scripts\python.exe` on Windows)

## VS Code Integration

The project includes `.vscode/settings.json` which automatically:
- Selects the `.venv` Python interpreter
- Activates the environment in new terminals
- Configures linting and formatting

If VS Code doesn't detect it:
1. Open Command Palette (Cmd+Shift+P / Ctrl+Shift+P)
2. Type "Python: Select Interpreter"
3. Choose `./.venv/bin/python`

## Automated Setup

Run the setup script to create and configure everything:

**macOS/Linux:**
```bash
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

## Troubleshooting

### "python3: command not found"
- Try `python` instead of `python3`
- Install Python from python.org

### "Permission denied" on setup.sh
```bash
chmod +x setup.sh
```

### Virtual environment won't activate
```bash
# Recreate it
rm -rf .venv
python3 -m venv .venv
```

### Packages not found after activation
```bash
# Make sure you're in the right environment
which python  # Should show .venv path

# Reinstall packages
pip install -r requirements.txt
```

## Best Practices

1. **Always activate before working**: `source .venv/bin/activate`
2. **Update requirements.txt** when adding packages: `pip freeze > requirements.txt`
3. **Don't commit .venv** to git (already in `.gitignore`)
4. **Use same Python version** across team (currently using Python 3.12.8)
5. **Recreate if corrupted**: Delete `.venv` and run `setup.sh` again

## Working with the Project

```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Run experiments
python scripts/run_experiment.py --experiment cv_screening

# 3. Evaluate results
python scripts/evaluate.py results/cv_screening_*.json

# 4. When done
deactivate
```

## IDE Support

### PyCharm
- File → Settings → Project → Python Interpreter
- Click gear icon → Add → Existing Environment
- Select `.venv/bin/python`

### VS Code
- Already configured via `.vscode/settings.json`
- Should auto-detect and activate

### Vim/Neovim
- Manually activate in terminal before opening editor
- Or use virtualenv plugins

## Dependencies Overview

Current project dependencies include:
- `openai`, `anthropic` - LLM providers
- `pandas`, `numpy` - Data processing
- `python-docx`, `PyPDF2` - Document handling
- `sentence-transformers`, `faiss-cpu` - Embeddings
- `plotly`, `dash`, `streamlit` - Visualization
- `pytest` - Testing

See `requirements.txt` for full list.
