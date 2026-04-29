param(
  [string]$TargetProject = "."
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$TargetSkills = Join-Path $TargetProject ".claude\skills"

New-Item -ItemType Directory -Force -Path $TargetSkills | Out-Null
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\req") $TargetSkills
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\gap") $TargetSkills
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\what") $TargetSkills

Write-Host "Installed TigerKit skills into: $TargetSkills"
Write-Host "Standalone commands may be available as: /req, /gap, /what"
