# Commands to Publish to GitHub

After creating your repository on GitHub, run these commands:

## Option 1: HTTPS (Recommended for beginners)

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Option 2: SSH (If you have SSH keys set up)

```bash
git remote add origin git@github.com:YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

## Replace:
- `YOUR_USERNAME` - Your GitHub username
- `REPO_NAME` - The name of the repository you created

## Example:
If your username is `johndoe` and repo name is `Alpaca05`:
```bash
git remote add origin https://github.com/johndoe/Alpaca05.git
git branch -M main
git push -u origin main
```
