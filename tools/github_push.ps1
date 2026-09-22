# Create the GitHub repository (if needed) and push the current branch to it.
#
#   powershell -ExecutionPolicy Bypass -File tools\github_push.ps1
#   powershell -ExecutionPolicy Bypass -File tools\github_push.ps1 -RepoName other-name -Private
#
# The script uses the GitHub credential that Git Credential Manager already stores on
# this machine. The token is never printed and never written to a file.
param(
    [string]$RepoName = "bankflow-ai-banking-assistant",
    [string]$Description = "BankFlow - AI Banking Assistant: full stack demo banking app built with React, Vite, Material UI and Django REST Framework, with JWT authentication, Recharts analytics and a rule based AI assistant.",
    [switch]$Private,
    [string]$ProjectPath = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"
$env:GIT_TERMINAL_PROMPT = "0"
$env:GCM_INTERACTIVE = "never"

# ---------------------------------------------------------------- credential
$raw = "protocol=https`nhost=github.com`n`n" | git credential fill 2>$null
$cred = @{}
foreach ($line in ($raw | Where-Object { $_ -match "=" })) {
    $parts = $line -split "=", 2
    $cred[$parts[0]] = $parts[1]
}
$token = $cred["password"]
if (-not $token) {
    throw "No GitHub credential found. Sign in once with Git Credential Manager, then run this script again."
}
$headers = @{
    Authorization          = "token $token"
    Accept                 = "application/vnd.github+json"
    "User-Agent"           = "BankFlow-Push"
}

# ------------------------------------------------------------------- account
$me = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $headers
Write-Output "Signed in to GitHub as $($me.login)"
$owner = $me.login

# ------------------------------------------------------------------ create
$repoUrl = "https://api.github.com/repos/$owner/$RepoName"
$exists = $true
try {
    $repo = Invoke-RestMethod -Uri $repoUrl -Headers $headers
} catch {
    $exists = $false
}

if ($exists) {
    Write-Output "Repository $owner/$RepoName already exists - pushing into it."
} else {
    $body = @{
        name        = $RepoName
        description = $Description
        private     = [bool]$Private
        has_issues  = $true
        has_wiki    = $false
    } | ConvertTo-Json
    $repo = Invoke-RestMethod -Method Post -Uri "https://api.github.com/user/repos" `
        -Headers $headers -ContentType "application/json" -Body $body
    Write-Output "Created repository $($repo.full_name) ($($repo.visibility))"
}

$topics = @("react", "django", "django-rest-framework", "jwt", "material-ui", "recharts",
            "banking-app", "full-stack", "demo-application")
try {
    Invoke-RestMethod -Method Put -Uri "$repoUrl/topics" -Headers $headers `
        -ContentType "application/json" -Body (@{ names = $topics } | ConvertTo-Json) | Out-Null
    Write-Output "Topics updated."
} catch {
    Write-Output "Topics could not be set (not important)."
}

# -------------------------------------------------------------------- push
Push-Location $ProjectPath
try {
    $remote = "https://github.com/$owner/$RepoName.git"
    if ((git remote) -contains "origin") {
        git remote remove origin | Out-Null
    }
    git remote add origin $remote
    Write-Output "Pushing to $remote"
    # git writes progress to stderr, so read it as text instead of letting it stop the script.
    $pushOutput = & git push -u origin HEAD 2>&1 | Out-String
    Write-Output $pushOutput.Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "git push failed with exit code $LASTEXITCODE"
    }
} finally {
    Pop-Location
}

# ------------------------------------------------------------------ verify
$final = Invoke-RestMethod -Uri $repoUrl -Headers $headers
Write-Output ""
Write-Output "Repository: $($final.html_url)"
Write-Output "Visibility: $($final.visibility)"
Write-Output "Default branch: $($final.default_branch)"
Write-Output "Size on GitHub: $([math]::Round($final.size / 1024, 1)) MB"
