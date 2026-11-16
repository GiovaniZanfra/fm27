<#
.SYNOPSIS
  Rebuilds the distilled JSON files in game_data/ from a Football Manager 27 install.

.EXAMPLE
  powershell -ExecutionPolicy Bypass -File game_data\extract\build.ps1
  powershell -ExecutionPolicy Bypass -File game_data\extract\build.ps1 -GameDir "E:\Games\Football Manager 27"

.NOTES
  Windows PowerShell 5.1 + libzstd.dll (ships with Git for Windows). Run it again after a game patch
  and review the git diff. Hand-written parts (role names, positions, summaries) live in role_notes.json.
#>
param(
    [string]$GameDir = "D:\SteamLibrary\steamapps\common\Football Manager 27",
    [string]$OutDir = (Split-Path $PSScriptRoot -Parent),
    [string]$ZstdDir = "C:\Program Files\Git\mingw64\bin"
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path (Join-Path $ZstdDir 'libzstd.dll'))) { throw "libzstd.dll not found in $ZstdDir (install Git for Windows or pass -ZstdDir)" }
$env:PATH = "$ZstdDir;$env:PATH"
if (-not ('Fmf' -as [type])) { Add-Type -Path (Join-Path $PSScriptRoot 'Fmf.cs') }

# ---------------------------------------------------------------- helpers

function Open-Fmf([string]$rel) {
    $path = Join-Path $GameDir $rel
    $data = [IO.File]::ReadAllBytes($path)
    @{ Data = $data; Entries = [Fmf]::ReadIndex($data); Rel = $rel }
}

function Read-Jsb($fmf, [string]$entryPath) {
    $e = $fmf.Entries | Where-Object { $_.Path -eq $entryPath } | Select-Object -First 1
    if (-not $e) { throw "$entryPath not found in $($fmf.Rel)" }
    [Fmf]::JsbToJson([Fmf]::ReadEntry($fmf.Data, $e)) | ConvertFrom-Json
}

function Read-Text($fmf, [string]$entryPath) {
    $e = $fmf.Entries | Where-Object { $_.Path -eq $entryPath } | Select-Object -First 1
    if (-not $e) { throw "$entryPath not found in $($fmf.Rel)" }
    [Text.Encoding]::UTF8.GetString([Fmf]::ReadEntry($fmf.Data, $e)).TrimStart([char]0xFEFF)
}

# Object properties in file order (ConvertFrom-Json keeps it).
function Props($o) { if ($null -eq $o) { @() } else { $o.PSObject.Properties } }

# Small JSON writer: stable, two-space indent, no \u escaping of ' < > &.
function To-Json($v, [int]$d = 0) {
    $pad = '  ' * ($d + 1); $end = '  ' * $d
    if ($null -eq $v) { return 'null' }
    if ($v -is [bool]) { return $(if ($v) { 'true' } else { 'false' }) }
    if ($v -is [string]) {
        $s = $v.Replace('\', '\\').Replace('"', '\"').Replace("`n", '\n').Replace("`r", '\r').Replace("`t", '\t')
        return '"' + $s + '"'
    }
    if ($v -is [int] -or $v -is [long] -or $v -is [double] -or $v -is [decimal]) {
        return ([double]$v).ToString('R', [Globalization.CultureInfo]::InvariantCulture)
    }
    if ($v -is [System.Collections.IDictionary]) {
        if ($v.Count -eq 0) { return '{}' }
        $items = foreach ($k in $v.Keys) { $pad + (To-Json ([string]$k)) + ': ' + (To-Json $v[$k] ($d + 1)) }
        return "{`n" + ($items -join ",`n") + "`n$end}"
    }
    if ($v -is [System.Collections.IEnumerable]) {
        $arr = @($v)
        if ($arr.Count -eq 0) { return '[]' }
        $simple = -not ($arr | Where-Object { $_ -is [System.Collections.IDictionary] -or ($_ -is [System.Collections.IEnumerable] -and $_ -isnot [string]) })
        if ($simple) { return '[' + (($arr | ForEach-Object { To-Json $_ ($d + 1) }) -join ', ') + ']' }
        $items = foreach ($x in $arr) { $pad + (To-Json $x ($d + 1)) }
        return "[`n" + ($items -join ",`n") + "`n$end]"
    }
    throw "To-Json: unsupported type $($v.GetType().FullName)"
}

$utf8 = New-Object System.Text.UTF8Encoding($false)
function Save([string]$name, $obj) {
    $path = Join-Path $OutDir $name
    [IO.File]::WriteAllText($path, (To-Json $obj) + "`n", $utf8)
    Write-Host "wrote $path"
}

# 'work_rate' -> 'Work Rate'; engine names that differ from the attribute screen are mapped.
$AttrRename = @{ movement = 'Off The Ball'; jumping = 'Jumping Reach'; team_work = 'Team Work'; teamwork = 'Team Work' }
function Attr-Name([string]$s) {
    if ($AttrRename.ContainsKey($s)) { return $AttrRename[$s] }
    (Get-Culture).TextInfo.ToTitleCase($s.Replace('_', ' '))
}

# ---------------------------------------------------------------- sources

# Game build number (Unity bundleVersion), e.g. 27.0.1.2503222.
$version = 'unknown'
$ggm = Join-Path $GameDir 'fm_Data\globalgamemanagers'
if (Test-Path $ggm) {
    $m = [regex]::Match([Text.Encoding]::ASCII.GetString([IO.File]::ReadAllBytes($ggm)), '\b2\d\.\d+\.\d+\.\d{5,}\b')
    if ($m.Success) { $version = $m.Value }
}

$simatch = Open-Fmf 'shared\data\simatch.fmf'
$training = Open-Fmf 'data\game_simulation\training.fmf'

$complexity = (Read-Jsb $simatch 'constants/generated_tactical_complexity_constants.jsb').root
$statMap = Read-Jsb $simatch 'qme_stat_relevant_attribute_data.jsb'
$sessions = Read-Jsb $training 'training_sessions.jsb'
$categories = Read-Jsb $training 'training_session_categories.jsb'
[xml]$styles = Read-Text $simatch 'tactics/styles.xml'

$notes = Get-Content (Join-Path $PSScriptRoot 'role_notes.json') -Raw -Encoding UTF8 | ConvertFrom-Json

# Role names defined in fm27/roles.py (the build warns about game roles missing there).
$rolesPy = Join-Path (Split-Path $OutDir -Parent) 'fm27\roles.py'
$harnessRoles = @{}
if (Test-Path $rolesPy) {
    foreach ($m in [regex]::Matches((Get-Content $rolesPy -Raw), '(?m)^\s+\("([^"]+)",\s*$')) { $harnessRoles[$m.Groups[1].Value] = $true }
}

$source = [ordered]@{ game = 'Football Manager 27'; version = $version }

# ---------------------------------------------------------------- roles.json

$skip = @('NO_ROLE', 'PRESSING_WNG_BACK')   # placeholder and a misspelt duplicate in the game enum
$roles = New-Object System.Collections.ArrayList
$problems = @()
foreach ($phase in @(@{ key = 'IP Role'; name = 'in_possession' }, @{ key = 'OOP Role'; name = 'out_of_possession' })) {
    $phaseNotes = $notes.($phase.name)
    foreach ($p in Props $complexity.Player.($phase.key)) {
        if ($skip -contains $p.Name) { continue }
        $n = $phaseNotes.($p.Name)
        if (-not $n) { $problems += "$($phase.name) $($p.Name): no entry in role_notes.json"; continue }
        if ($harnessRoles.Count -and -not $harnessRoles[$n.harness]) { $problems += "$($n.harness): not defined in fm27/roles.py" }
        [void]$roles.Add([ordered]@{
            id          = $p.Name
            phase       = $phase.name
            name        = $n.name
            harness     = $n.harness
            score_column = ($n.harness -replace ' ', '_') + '_Score'
            positions   = @($n.positions)
            complexity  = $p.Value
            summary     = $n.summary
        })
    }
    foreach ($k in Props $phaseNotes) {
        if (-not ($complexity.Player.($phase.key).PSObject.Properties.Name -contains $k.Name)) { $problems += "$($phase.name) $($k.Name): in role_notes.json but not in the game" }
    }
}
$problems | ForEach-Object { Write-Warning $_ }

Save 'roles.json' ([ordered]@{
    source = $source
    notes = @(
        'id and complexity come from the game (simatch.fmf, generated_tactical_complexity_constants).',
        'name, harness, positions and summary are hand-written in extract/role_notes.json.',
        'complexity: tactical complexity cost of the role (0-3); the game caps a player at 4 including his instructions.'
    )
    counts = [ordered]@{
        in_possession = @($roles | Where-Object { $_.phase -eq 'in_possession' }).Count
        out_of_possession = @($roles | Where-Object { $_.phase -eq 'out_of_possession' }).Count
    }
    roles = $roles
})

# ---------------------------------------------------------------- instructions.json

# Phase of each team instruction group, as laid out on the tactics screen (annotation, not game data).
$teamPhase = @{
    'Passing Style' = 'in_possession'; Tempo = 'in_possession'; Width = 'in_possession'; 'Focus Play' = 'in_possession'
    'Passing Strategy' = 'in_possession'; 'Look For' = 'in_possession'; 'Build up Play' = 'in_possession'; Crossing = 'in_possession'
    Dribbling = 'in_possession'; Shooting = 'in_possession'; 'Creative Freedom' = 'in_possession'; 'Waste Time' = 'in_possession'
    GOALKEEPER_UP_FOR_ATTACKING_SET_PIECES = 'in_possession'
    Transition = 'in_transition'; 'Defence Transition' = 'in_transition'; 'GK Distribution' = 'in_transition'
    'Line of Engagement' = 'out_of_possession'; 'Defensive Line' = 'out_of_possession'; Line = 'out_of_possession'
    'Pressing Intensity' = 'out_of_possession'; 'Pressing Trap' = 'out_of_possession'; Tackling = 'out_of_possession'
    'Defending Crosses' = 'out_of_possession'; PREVENT_SHORT_GOALKEEPER_DISTRIBUTION = 'out_of_possession'
}
$playerPhase = @{ Marking = 'out_of_possession'; 'Pressing Intensity' = 'out_of_possession'; Tackling = 'out_of_possession' }

function Options($obj) {
    $o = [ordered]@{}
    foreach ($p in Props $obj) {
        if ($p.Value -is [System.Management.Automation.PSCustomObject]) { $o[$p.Name] = Options $p.Value } else { $o[$p.Name] = $p.Value }
    }
    $o
}

$team = [ordered]@{}
$teamScalars = [ordered]@{}
foreach ($p in Props $complexity.Team) {
    if ($p.Value -is [System.Management.Automation.PSCustomObject]) {
        $ph = $teamPhase[$p.Name]; if (-not $ph) { $ph = 'unknown' }
        $team[$p.Name] = [ordered]@{ phase = $ph; options = Options $p.Value }
    } elseif (@('MAX', 'MIN', 'DEFAULT', 'NONE') -contains $p.Name) {
        $teamScalars[$p.Name] = $p.Value
    } else {
        $ph = $teamPhase[$p.Name]; if (-not $ph) { $ph = 'unknown' }
        $team[$p.Name] = [ordered]@{ phase = $ph; toggle = $true; complexity = $p.Value }
    }
}
$player = [ordered]@{}
foreach ($p in Props $complexity.Player.Instructions) {
    if ($p.Value -is [System.Management.Automation.PSCustomObject]) {
        $ph = $playerPhase[$p.Name]; if (-not $ph) { $ph = 'in_possession' }
        $player[$p.Name] = [ordered]@{ phase = $ph; options = Options $p.Value }
    }
}
Save 'instructions.json' ([ordered]@{
    source = $source
    notes = @(
        'Every option is the game enum name; its number is the tactical complexity it adds (from generated_tactical_complexity_constants).',
        'Each group allows one option or none. phase is our annotation of where the group sits on the tactics screen.',
        'Team complexity is clamped to limits.team_min..team_max; a player carries role + instructions up to limits.max_complexity_per_player.'
    )
    limits = [ordered]@{
        team_min = $teamScalars.MIN; team_max = $teamScalars.MAX; team_default = $teamScalars.DEFAULT
        player_default = $complexity.Player.DEFAULT
        max_complexity_per_player = $complexity.Opposition.MAX_COMPLEXITY_PER_PLAYER
        max_players_for_opposition_complexity = $complexity.Opposition.MAX_PLAYERS_FOR_COMPLEXITY
    }
    team = $team
    player = $player
})

# ---------------------------------------------------------------- stat_attributes.json

$stats = [ordered]@{}
foreach ($v in $statMap.values) { $stats[$v.stat_type] = @($v.relevant_attributes | ForEach-Object { Attr-Name $_ }) }
$byAttr = [ordered]@{}
foreach ($k in $stats.Keys) { foreach ($a in $stats[$k]) { if (-not $byAttr.Contains($a)) { $byAttr[$a] = New-Object System.Collections.ArrayList }; [void]$byAttr[$a].Add($k) } }
$sortedByAttr = [ordered]@{}
foreach ($a in ($byAttr.Keys | Sort-Object)) { $sortedByAttr[$a] = @($byAttr[$a]) }
Save 'stat_attributes.json' ([ordered]@{
    source = $source
    notes = @(
        'Which attributes the quick match engine ties to each match statistic (simatch.fmf, qme_stat_relevant_attribute_data).',
        'Attribute names are converted to the names on the attribute screen and in data/*/interim/attributes.csv (movement -> Off The Ball, jumping -> Jumping Reach). Dirtiness is a hidden attribute.'
    )
    stat_to_attributes = $stats
    attribute_to_stats = $sortedByAttr
})

# ---------------------------------------------------------------- training.json

$sess = New-Object System.Collections.ArrayList
foreach ($s in $sessions.data_array) {
    $attrs = [ordered]@{}
    foreach ($g in Props $s.attributes) { if (@($g.Value).Count) { $attrs[$g.Name] = @($g.Value) } }
    [void]$sess.Add([ordered]@{
        name = $s.name; category = $s.category
        attributes = $attrs
        condition = $s.condition; fatigue = $s.fatigue; injuries = $s.injuries; happiness = $s.happiness; sharpness = $s.sharpness
        max_sessions_per_week = $s.max_sessions_per_week
        ignores_category_limits = $s.ignores_category_limits
    })
}
$cats = @($categories.data_array | ForEach-Object { [ordered]@{ category = $_.category; max_sessions_per_week = $_.max_sessions_per_week; counts_towards_match_limits = $_.considers_limits_per_match } })
Save 'training.json' ([ordered]@{
    source = $source
    notes = @(
        'From training.fmf (training_sessions, training_session_categories).',
        'attributes: what the session trains, per position group (attacking, defensive, goalkeeping, midfield); sessions without attributes train tactics, condition or nothing.',
        'condition, fatigue, injuries, happiness, sharpness: impact on the player from -3 to 3, positive = good for him (Rest: condition 3, fatigue 1; Heavy Conditioning: fatigue -3, injuries -2 = higher injury risk).'
    )
    categories = $cats
    sessions = $sess
})

# ---------------------------------------------------------------- tactic_presets.json

function Clean([string]$s) { ($s -replace '\[COMMENT:[^\]]*\]', '').Trim() }
$presets = New-Object System.Collections.ArrayList
foreach ($rec in $styles.record.record) {
    $folder = $rec.folder
    $tacs = @($simatch.Entries | Where-Object { $_.Folder -eq "tactics/$folder" -and $_.Ext -eq '.tac' } | Sort-Object { [int]($_.Name -replace '--.*$', '') })
    $pairs = @(foreach ($t in $tacs) {
        $body = ($t.Name -replace '^\d+--', '') -replace ' - [^-]+$', ''
        $parts = $body -split ' _ '
        [ordered]@{ in_possession = $parts[0].Trim(); out_of_possession = $parts[1].Trim() }
    })
    $name = Clean (($rec.translation | Where-Object { $_.id -eq 'text' }).value)
    $tags = @($rec.list | Where-Object { $_.id -eq 'description' } | ForEach-Object { $_.translation } | ForEach-Object { Clean $_.value })
    [void]$presets.Add([ordered]@{ id = $rec.tactical_style_id; name = $name; tags = $tags; formations = $pairs })
}
Save 'tactic_presets.json' ([ordered]@{
    source = $source
    notes = @(
        'Tactical styles and the formation pairs the game offers as presets (simatch.fmf, tactics/). Each pair is in-possession shape _ out-of-possession shape.',
        'The .tac files with the preset roles and instructions are binary and not decoded yet.'
    )
    styles = $presets
})

if ($problems) { Write-Warning "$($problems.Count) role(s) need attention in role_notes.json" }
