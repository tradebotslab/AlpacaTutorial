# publish_to_github.ps1
# PowerShell script to publish the repository to GitHub
# Usage: .\publish_to_github.ps1 -Username "YOUR_USERNAME" -RepoName "REPO_NAME"

param(
    [Parameter(Mandatory=$true)]
    [string]$Username,
    
    [Parameter(Mandatory=$true)]
    [string]$RepoName,
    
    [Parameter(Mandatory=$false)]
    [switch]$UseSSH
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Publishing to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if remote already exists
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "Remote 'origin' already exists: $remoteExists" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/n)"
    if ($overwrite -eq "y" -or $overwrite -eq "Y") {
        git remote remove origin
    } else {
        Write-Host "Aborted." -ForegroundColor Red
        exit 1
    }
}

# Set remote URL
if ($UseSSH) {
    $remoteUrl = "git@github.com:$Username/$RepoName.git"
    Write-Host "Using SSH: $remoteUrl" -ForegroundColor Green
} else {
    $remoteUrl = "https://github.com/$Username/$RepoName.git"
    Write-Host "Using HTTPS: $remoteUrl" -ForegroundColor Green
}

# Add remote
Write-Host ""
Write-Host "Adding remote..." -ForegroundColor Yellow
git remote add origin $remoteUrl

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to add remote!" -ForegroundColor Red
    exit 1
}

# Rename branch to main if needed
Write-Host "Checking branch..." -ForegroundColor Yellow
$currentBranch = git branch --show-current
if ($currentBranch -ne "main") {
    Write-Host "Renaming branch from '$currentBranch' to 'main'..." -ForegroundColor Yellow
    git branch -M main
}

# Push to GitHub
Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "You may be prompted for your GitHub credentials." -ForegroundColor Cyan
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Successfully published to GitHub!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Repository URL: https://github.com/$Username/$RepoName" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Failed to push to GitHub!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please make sure:" -ForegroundColor Yellow
    Write-Host "1. The repository exists on GitHub" -ForegroundColor Yellow
    Write-Host "2. You have the correct permissions" -ForegroundColor Yellow
    Write-Host "3. Your credentials are correct" -ForegroundColor Yellow
    exit 1
}
