# Tutorial 1: Your First Step – Generating API Keys in Alpaca

Welcome to the Alpaca Trading Course! This is your very first step into the exciting world of algorithmic trading. Before we write any code, we need to set up your developer environment. This involves creating an account with Alpaca and generating the necessary API keys that will allow your bot to communicate with their trading platform.

Crucially, we'll start with **paper trading**, which uses simulated money in a live market environment. This means you can test your strategies without any financial risk.

## 📋 What are API Keys?

An **API Key** (Application Programming Interface Key) is like a password that authenticates your trading bot with Alpaca's servers. It tells Alpaca who you are and that you have permission to send trading commands (like buying or selling stocks) or request market data.

You'll typically generate two keys:

- **API Key ID**: A public identifier.
- **Secret API Key**: A private key that must be kept absolutely confidential. Never share it or expose it in your code!

## 🚀 Step-by-Step Guide: Creating Your Alpaca Account

### Step 1: Go to Alpaca's Website

Open your web browser and navigate to [https://alpaca.markets/](https://alpaca.markets/).

### Step 2: Sign Up

Look for a "Sign Up" or "Get Started" button (it's often prominent on the homepage). Click it to begin the registration process.

### Step 3: Choose Account Type

You'll likely be given an option to create a Live Trading account or a Paper Trading account. **Select the "Paper Trading" option** to start without real money.

> **Note:** Even if you initially choose Paper Trading, you can often upgrade to Live Trading later if you wish.

### Step 4: Enter Your Details

Fill in the required information, such as your email address, create a password, and agree to their terms of service.

### Step 5: Verify Your Email

Alpaca will send a verification email to the address you provided. Open this email and click the verification link to activate your account.

## 🔑 Step-by-Step Guide: Generating Your Paper Trading API Keys

Once your account is created and verified, you can log in and generate your API keys.

### Step 1: Log In to Alpaca

Go back to [https://alpaca.markets/](https://alpaca.markets/) and log in using your newly created credentials.

### Step 2: Navigate to the Dashboard

After logging in, you'll land on your Alpaca dashboard.

### Step 3: Switch to Paper Account

On the top right corner of the dashboard, you should see a toggle or a dropdown menu that says "Live" or "Paper". **Ensure you are switched to the "Paper" account.** This is crucial for generating keys that work with the paper trading environment.

### Step 4: Find API Keys Section

Look for a section related to "API Keys" or "Key Management" in the left-hand navigation sidebar. It's often under a "Settings" or "Account" menu.

### Step 5: Generate New Key

Click on the button to "Generate New Key" or "Create Key".

### Step 6: Record Your Keys

Alpaca will display your:

- **API Key ID**
- **Secret API Key**

> ⚠️ **IMPORTANT:** These keys are usually shown only once. Copy both the API Key ID and the Secret API Key immediately and save them in a secure location. A text file on your local machine that is NOT publicly accessible is a good temporary place. You will need these for every trading bot you build.

> ⚠️ **SECURITY WARNING:** Do NOT share these keys with anyone, and do not commit them directly into a public code repository like GitHub.

## 📁 Project Structure

```
Alpaca01/
│
├── Instructions.md        # Detailed tutorial instructions
├── README.md             # This documentation
├── config.example.py     # Template for configuration file
├── requirements.txt      # Python dependencies (if needed)
└── .gitignore           # Git ignore rules
```

## ⚙️ Configuration Template

After generating your API keys, you'll need to create a `config.py` file for future tutorials. Use the provided `config.example.py` as a template:

1. Copy `config.example.py` to `config.py`:
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

## 🔒 Security Best Practices

- ⚠️ **Never commit `config.py` to Git** - Add it to `.gitignore`
- ⚠️ **Never share your API keys** publicly or in screenshots
- ⚠️ **Use Paper Trading keys** for tutorials (not Live Trading)
- ⚠️ **Rotate your keys** if you suspect they've been compromised
- ⚠️ **Store keys securely** - Consider using environment variables or a secure password manager

## 📚 Next Steps

Once you've successfully created your Alpaca account and generated your API keys, you're ready to proceed to:

- **Tutorial 2**: Connect to Alpaca and check your account status
- **Tutorial 3+**: Start building your first trading bot

## 🐛 Troubleshooting

### Problem: I can't find the API Keys section

**Solution:**
- Make sure you're logged into your Alpaca account
- Check the left sidebar navigation menu
- Look under "Settings" or "Account" sections
- Try accessing directly: [https://app.alpaca.markets/paper/dashboard/overview](https://app.alpaca.markets/paper/dashboard/overview)

### Problem: I generated keys but can't see them again

**Solution:**
- API keys are typically shown only once for security reasons
- You'll need to generate new keys if you didn't save them
- Make sure to copy them immediately when they're displayed

### Problem: I'm not sure if I'm in Paper Trading mode

**Solution:**
- Look for a toggle or dropdown in the top right corner of the dashboard
- It should clearly indicate "Paper" or "Live"
- Make sure it's set to "Paper" before generating keys

## ✅ Verification Checklist

Before moving to the next tutorial, make sure you have:

- [ ] Created an Alpaca account
- [ ] Verified your email address
- [ ] Switched to Paper Trading mode
- [ ] Generated API Key ID
- [ ] Generated Secret API Key
- [ ] Saved both keys in a secure location
- [ ] Created `config.py` from `config.example.py` (for next tutorial)
- [ ] Added `config.py` to `.gitignore` (if using Git)

## 📞 Support

If you encounter issues:

1. Check the [Alpaca Documentation](https://alpaca.markets/docs/)
2. Visit the [Alpaca Support Center](https://alpaca.markets/support)
3. Review the error messages for specific details
4. Ensure all steps were followed correctly

## 📝 Conclusion

You've successfully created your Alpaca account and generated your API keys for paper trading! You now have the credentials needed to start building and testing your algorithmic trading strategies without risking real money. Keep these keys safe, as they are your bot's identity and access to the market.

In the next lesson, we will begin setting up your Python development environment and write your very first lines of code to connect to Alpaca.

## 📝 License

This tutorial is part of an educational course on algorithmic trading with Alpaca.

---

**"The goal of a successful trader is to make the best trades. Money is secondary." - Alexander Elder**

