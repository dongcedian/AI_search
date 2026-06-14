# setup_scheduler.ps1
# Creates a Windows Task Scheduler task to run AI News daily at 8 AM.
# Run this in an ADMIN PowerShell window.

$taskName = "AI News Daily Fetch"
$scriptPath = Join-Path $PSScriptRoot "ai_news.py"
$pythonExe = (Get-Command python -ErrorAction Stop).Source
$workingDir = $PSScriptRoot

$action = New-ScheduledTaskAction `
    -Execute $pythonExe `
    -Argument "`"$scriptPath`" --output-dir `"$workingDir\output`"" `
    -WorkingDirectory $workingDir

$trigger = New-ScheduledTaskTrigger -Daily -At 8:00AM

$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Fetch AI news from RSS feeds and generate an HTML digest each morning."

Write-Host "Task '$taskName' created successfully!" -ForegroundColor Green
Write-Host "It will run daily at 8:00 AM." -ForegroundColor Green
Write-Host "To test it now, run: python ai_news.py" -ForegroundColor Yellow
