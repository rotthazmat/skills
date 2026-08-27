#Requires -Version 5.1
<#
.SYNOPSIS
    Symlinks this skills/ repo into ~/.claude/skills and ~/.agents/skills.

.DESCRIPTION
    Creates (or recreates) a "skills" symlink inside both ~/.claude and ~/.agents
    pointing at this repository. Missing ~/.claude or ~/.agents directories are
    created. An existing symlink is replaced; an existing real folder is left
    untouched and reported as an error.

    Compatible with Windows PowerShell 5.1 and PowerShell 7+.
    On Windows, creating symlinks requires Developer Mode or an elevated shell.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$SourceDir = $PSScriptRoot
$HomeDir   = if ($env:HOME) { $env:HOME } else { $env:USERPROFILE }

function Write-Red   ($m) { Write-Host $m -ForegroundColor Red }
function Write-Green ($m) { Write-Host $m -ForegroundColor Green }
function Write-Cyan  ($m) { Write-Host $m -ForegroundColor Cyan }

function Test-IsSymlink ($item) {
    if ($null -eq $item) { return $false }
    if ($item.LinkType -eq 'SymbolicLink') { return $true }
    return $item.Attributes.HasFlag([System.IO.FileAttributes]::ReparsePoint)
}

$exitCode = 0

foreach ($name in @('.claude', '.agents')) {
    $base = Join-Path $HomeDir $name

    if (-not (Test-Path -LiteralPath $base)) {
        New-Item -ItemType Directory -Path $base | Out-Null
        Write-Cyan "Created $base"
    }

    $link = Join-Path $base 'skills'
    $item = Get-Item -LiteralPath $link -Force -ErrorAction SilentlyContinue

    if (Test-IsSymlink $item) {
        $item.Delete()
        Write-Cyan "Removed existing symlink $link"
        $item = $null
    }

    if ($null -ne $item) {
        Write-Red "There's already a skills/ folder inside $base"
        $exitCode = 1
        continue
    }

    try {
        New-Item -ItemType SymbolicLink -Path $link -Target $SourceDir | Out-Null
        Write-Green "Linked $link -> $SourceDir"
    }
    catch {
        Write-Red "Failed to create symlink $link : $($_.Exception.Message)"
        Write-Red "On Windows, enable Developer Mode or run this script from an elevated shell."
        $exitCode = 1
    }
}

exit $exitCode
