# Lesson 22: **Stop Digging in the Code – Using an External Config File**

Welcome to Lesson 22 of the Alpaca Trading Course! This lesson teaches you one of the most important professional practices in software development: separating configuration from code. You'll learn how to move API keys and strategy parameters to an external JSON file, making your bot more secure, flexible, and maintainable.

## The Problem: Hardcoded Settings in Code

Until now, you've likely kept API keys and parameters directly in your Python code. This is problematic: you must dig through code to change settings, accidentally sharing code on GitHub exposes your API keys, settings get scattered across multiple files, and configuration is mixed with logic, making code harder to maintain.

| Problem/Challenge | Description |
|---|---|
| **Lack of Flexibility** | Want to change symbol or parameters? You dig through code |
| **Security Risk** | Accidentally sharing code on GitHub exposes your API keys |
| **Management Difficulty** | Settings get scattered across multiple files as bot grows |
| **No Separation of Concerns** | Configuration mixed with logic makes code harder to maintain |

## The Solution: External Configuration File (JSON)

The solution is to separate configuration from application logic using a `config.json` file. This provides: more security (API keys separated from code), more flexibility (change parameters without modifying logic), better organization (all settings in one place), team-friendly (different members can use different configs), and easier testing (switch between test/production configs easily).

### Step 22.1: Install Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `alpaca-py` - Alpaca's official Python SDK
- `pandas` - Data manipulation for historical analysis
- `requests` - HTTP library (dependency)

### Step 22.2: Create Your Configuration File

1. Copy the example config:
   ```bash
   cp config.example.json config.json
   ```

2. Edit `config.json` with your settings:
   ```json
   {
     "api_key": "YOUR_API_KEY",
     "api_secret": "YOUR_API_SECRET",
     "paper_trading": true,
     "trade_symbol": "SPY",
     "trade_quantity": 10,
     "strategy_parameters": {
       "short_window": 40,
       "long_window": 100
     }
   }
   ```

⚠️ **IMPORTANT:** Never commit `config.json` to Git! Add it to `.gitignore`.

### Step 22.3: Run the Config-Based Bot

Execute the bot:

```bash
python config_bot.py
```

The bot will load all settings from `config.json` instead of hardcoded values.

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Never Commit Config Files** | Add `config.json` to `.gitignore` to protect API keys |
| **Use Example Templates** | Provide `config.example.json` as a template without real keys |
| **Validate Config on Load** | Check that required fields exist and have valid values |
| **Separate Concerns** | Keep all configuration in one file, separate from logic |
| **Environment-Specific Configs** | Use different config files for development, testing, and production |

## Conclusion

You've successfully learned how to use external configuration files! This professional practice separates settings from code, making your bot more secure, flexible, and maintainable. You'll never hardcode settings again. In the next lesson, you'll learn how to manage bot state persistence so your bot remembers its position across restarts.
