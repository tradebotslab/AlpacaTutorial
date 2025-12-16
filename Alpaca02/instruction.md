# Tutorial 2: "Hello, Alpaca!" – Connect & Check Your Account Status

**Goal:** In this tutorial, you will write your very first Python script to connect to the Alpaca API and retrieve basic information about your paper trading account, such as your current equity (total value). This is the fundamental step for any automated trading bot.

---

## 1. Prerequisites

Before you start, make sure you have:

*   **Python Installed:** Python 3.8+ (preferably 3.10 or newer).
*   **An IDE/Code Editor:** Visual Studio Code, PyCharm, or any other editor you prefer.
*   **Alpaca Paper Trading Account & API Keys:** You should have completed **Tutorial 1** and generated your `API_KEY` and `SECRET_KEY` for your paper trading account.
*   **`alpaca-trade-api-python` library installed:** If not, open your terminal/command prompt and run:
    ```bash
    pip install alpaca-trade-api-python
    ```

---

## 2. Project Setup

Let's organize your project. Create a new folder for this tutorial, for example: `alpaca_bot_project/tutorial_02_hello_alpaca`.

Inside this folder, create two files:
1.  `config.py` (This will store your sensitive API keys securely)
2.  `hello_alpaca.py` (This will be your main script)

---

## 3. Configure Your API Keys (`config.py`)

Open `config.py` and add your Alpaca API keys and the base URL for paper trading. **Replace the placeholder values** with your actual keys from Tutorial 1.

```python
# config.py

# Alpaca API Keys for the paper trading account
API_KEY = "YOUR_PAPER_API_KEY_HERE"  # <--- REPLACE WITH YOUR API KEY
SECRET_KEY = "YOUR_PAPER_SECRET_KEY_HERE" # <--- REPLACE WITH YOUR SECRET KEY

# Always default to the paper trading URL for tutorials
BASE_URL = "https://paper-api.alpaca.markets"

# IMPORTANT: Never share this file or upload it to public repositories like GitHub!
