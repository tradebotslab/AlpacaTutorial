# How to Publish to GitHub

## 🚀 Recommended Method: Add Folder to Main Repository

All tutorials (Alpaca13, Alpaca14, Alpaca15, etc.) should be in ONE repository as separate folders.

### Quick Steps:

```powershell
# 1. Navigate to main AlpacaTutorial folder
cd "C:\Users\tcieslar004\OneDrive - PwC\Desktop\Projekty\AlpacaTradingCourse\AlpacaTutorial"

# 2. Remove local .git from tutorial folder (if exists)
Remove-Item -Recurse -Force "AlpacaXX\.git"

# 3. Add the folder
git add AlpacaXX/

# 4. Commit
git commit -m "Add Tutorial XX (AlpacaXX) - Tutorial Name"

# 5. Push to GitHub
git push origin main
```

### Example for Tutorial 13, 14, 15:
```powershell
git add Alpaca13/
git commit -m "Add Tutorial 13 (Alpaca13) - Dynamic Position Sizing"
git push origin main
```

```powershell
git add Alpaca14/
git commit -m "Add Tutorial 14 (Alpaca14) - Trailing Stop Loss"
git push origin main
```

```powershell
git add Alpaca15/
git commit -m "Add Tutorial 15 (Alpaca15) - Multiple Timeframes"
git push origin main
```

---

## 🔒 Security - What Gets Published

### ✅ What WILL be published:
- Bot source code
- README.md
- requirements.txt
- instructions.md
- config.example.py (template)
- .gitignore

### ❌ What will NOT be published (protected by .gitignore):
- config.py (contains your API keys) ⚠️
- .cursorrules (IDE configuration)
- __pycache__/ (Python cache)
- *.log (log files)

---

## 📁 Repository Structure

Your repository will have this structure:

```
AlpacaTutorial/
├── Alpaca02/
├── Alpaca04/
├── Alpaca13/
├── Alpaca14/
├── Alpaca15/
└── ...
```

Each folder is a complete, standalone tutorial!


