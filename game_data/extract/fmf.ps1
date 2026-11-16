<#
.SYNOPSIS
  Lists or unpacks a Football Manager 27 .fmf container.

.EXAMPLE
  .\fmf.ps1 -Fmf "D:\SteamLibrary\steamapps\common\Football Manager 27\shared\data\simatch.fmf" -List
  .\fmf.ps1 -Fmf "...\simatch.fmf" -OutDir raw\simatch            # every file; .jsb also as .json
  .\fmf.ps1 -Fmf "...\simatch.fmf" -OutDir raw\simatch -Only qme_stat_relevant_attribute_data

.NOTES
  Needs libzstd.dll. Git for Windows ships one (C:\Program Files\Git\mingw64\bin); pass -ZstdDir otherwise.
  Runs on Windows PowerShell 5.1 (the C# in Fmf.cs is compiled on the fly).
#>
param(
    [Parameter(Mandatory = $true)][string]$Fmf,
    [string]$OutDir,
    [switch]$List,
    [string[]]$Only,
    [string]$ZstdDir = "C:\Program Files\Git\mingw64\bin"
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path (Join-Path $ZstdDir 'libzstd.dll'))) { throw "libzstd.dll not found in $ZstdDir (install Git for Windows or pass -ZstdDir)" }
$env:PATH = "$ZstdDir;$env:PATH"
if (-not ('Fmf' -as [type])) { Add-Type -Path (Join-Path $PSScriptRoot 'Fmf.cs') }

$data = [IO.File]::ReadAllBytes((Resolve-Path $Fmf))
$entries = [Fmf]::ReadIndex($data)

if ($List -or -not $OutDir) {
    $entries | ForEach-Object { '{0,10}  {1}' -f $_.Size, $_.Path }
    return
}

New-Item -ItemType Directory -Force $OutDir | Out-Null
$utf8 = New-Object System.Text.UTF8Encoding($false)
foreach ($e in $entries) {
    if ($Only -and ($Only -notcontains $e.Name)) { continue }
    $bytes = [Fmf]::ReadEntry($data, $e)
    $dir = if ($e.Folder) { Join-Path $OutDir $e.Folder } else { $OutDir }
    New-Item -ItemType Directory -Force $dir | Out-Null
    if ($e.Ext -eq '.jsb') {
        try {
            [IO.File]::WriteAllText((Join-Path $dir ($e.Name + '.json')), [Fmf]::JsbToJson($bytes), $utf8)
            continue
        } catch {
            Write-Warning "$($e.Path): $($_.Exception.InnerException.Message) - kept as .jsb"
        }
    }
    [IO.File]::WriteAllBytes((Join-Path $dir $e.FileName), $bytes)
}
