$ErrorActionPreference = "Stop"
$python = "C:\Users\stephenxxy\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$items = @(
  @{ item = "F01_1daycloud"; run = "gwdg_qwen3_omni_30b_v15_f01_smoke" },
  @{ item = "F03_about_gitlab"; run = "gwdg_qwen3_omni_30b_v15_f03_smoke" },
  @{ item = "F06_community_dynamics"; run = "gwdg_qwen3_omni_30b_v15_f06_smoke" },
  @{ item = "F09_elections_bc"; run = "gwdg_qwen3_omni_30b_v15_f09_smoke" }
)
foreach ($entry in $items) {
  $stamp = Get-Date -Format o
  Write-Output "[$stamp] START $($entry.item) $($entry.run)"
  & $python scripts\generate_track_b_ui.py --item $entry.item --provider gwdg-openai --model qwen3-omni-30b-a3b-instruct --prompt-id TB-GEN-v15 --max-tokens 20000 --run-name $entry.run
  $code = $LASTEXITCODE
  $stamp = Get-Date -Format o
  Write-Output "[$stamp] EXIT $($entry.item) $($entry.run) code=$code"
  if ($code -ne 0) { exit $code }
}
