param(
  [string]$TargetProject = "."
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$TargetSkills = Join-Path $TargetProject ".claude\skills"

New-Item -ItemType Directory -Force -Path $TargetSkills | Out-Null
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\gap") $TargetSkills
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\gaplan") $TargetSkills
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\go") $TargetSkills
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\next") $TargetSkills
Copy-Item -Recurse -Force (Join-Path $RepoRoot "skills\plan") $TargetSkills

Write-Host "Installed tigap skills into: $TargetSkills"
Write-Host "Standalone commands may be available as: /gap, /gaplan, /go, /next, /plan"
