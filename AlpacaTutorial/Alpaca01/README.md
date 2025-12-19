# Lesson 1: **Generating API Keys in Alpaca**

Welcome to Lesson 1 of the Alpaca Trading Course! This is your very first step into the exciting world of algorithmic trading. Before we write any code, we need to set up your developer environment. This involves creating an account with Alpaca and generating the necessary API keys that will allow your bot to communicate with their trading platform. Crucially, we'll start with **paper trading**, which uses simulated money in a live market environment. This means you can test your strategies without any financial risk.

## The Problem: Trading Without Proper Authentication

Without API keys, you cannot programmatically interact with Alpaca's trading platform. You would be limited to manual trading through the web interface, which prevents automation and algorithmic strategies.

| Problem/Challenge | Description |
|---|---|
| **No Programmatic Access** | Without API keys, you cannot write code to automate trading decisions or execute trades programmatically |
| **Manual Trading Limitations** | Manual trading through a web interface is slow, error-prone, and cannot run 24/7 |
| **No Testing Environment** | Without paper trading keys, you would have to risk real money to test your strategies |
| **Security Risks** | Improperly managed API keys can expose your account to unauthorized access |

## The Solution: Generate Secure API Keys for Paper Trading

The solution is to create an Alpaca account and generate API keys specifically for paper trading. API keys are like passwords that authenticate your trading bot with Alpaca's servers. They tell Alpaca who you are and that you have permission to send trading commands or request market data. You'll generate two keys: an **API Key ID** (public identifier) and a **Secret API Key** (private key that must be kept absolutely confidential).

### Step 1.1: Create Your Alpaca Account

1. Open your web browser and navigate to [https://alpaca.markets/](https://alpaca.markets/)
2. Look for a "Sign Up" or "Get Started" button and click it
3. Choose the "Paper Trading" option to start without real money
4. Fill in the required information (email, password, etc.) and agree to terms of service
5. Verify your email address by clicking the verification link sent to your email

### Step 1.2: Generate Your Paper Trading API Keys

1. Log in to your Alpaca account at [https://alpaca.markets/](https://alpaca.markets/)
2. On the top right corner, ensure you are switched to the "Paper" account (not "Live")
3. Navigate to the "API Keys" or "Key Management" section (usually under "Settings" or "Account")
4. Click "Generate New Key" or "Create Key"
5. Copy both the **API Key ID** and **Secret API Key** immediately and save them securely

⚠️ **IMPORTANT:** These keys are usually shown only once. Never share them publicly or commit them to version control.

### Step 1.3: Configure Your Development Environment

1. Copy the example configuration file:
   ```bash
   cp config.example.py config.py
   ```

2. Open `config.py` and replace the placeholder values with your actual API keys:
   ```python
   API_KEY = "YOUR_ACTUAL_API_KEY_ID_HERE"
   SECRET_KEY = "YOUR_ACTUAL_SECRET_KEY_HERE"
   BASE_URL = "https://paper-api.alpaca.markets"
   ```

3. **Never commit `config.py` to version control!** It should be in `.gitignore`.

## Best Practices / Important Considerations

| Tip/Consideration | Description |
|---|---|
| **Use Paper Trading First** | Always start with paper trading keys to test strategies without financial risk |
| **Never Commit Keys** | Add `config.py` to `.gitignore` and never share your API keys publicly |
| **Rotate Keys Regularly** | If you suspect keys have been compromised, generate new ones immediately |
| **Store Keys Securely** | Use a secure password manager or encrypted storage, not plain text files in public locations |
| **Separate Paper and Live Keys** | Use different keys for paper trading and live trading to prevent accidental real-money trades |

## Conclusion

You've successfully created your Alpaca account and generated your API keys for paper trading! You now have the credentials needed to start building and testing your algorithmic trading strategies without risking real money. Keep these keys safe, as they are your bot's identity and access to the market. In the next lesson, we will begin setting up your Python development environment and write your very first lines of code to connect to Alpaca.
