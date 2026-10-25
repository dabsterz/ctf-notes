# Exercises the documented field mapping with synthetic XML, not a real EVTX parser.
$guideRoot = Split-Path $PSScriptRoot -Parent
$quickText = Get-Content -LiteralPath (Join-Path $guideRoot 'QUICKSTART.md') -Raw -Encoding UTF8
$blocks = [regex]::Matches($quickText, '(?ms)^```powershell\r?\n(.*?)^```')
foreach ($block in $blocks) {
    $parseTokens = $null
    $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseInput($block.Groups[1].Value, [ref]$parseTokens, [ref]$parseErrors) | Out-Null
    if ($parseErrors.Count -ne 0) { throw ($parseErrors | Out-String) }
}
$eventBlock = @($blocks | Where-Object { $_.Groups[1].Value.StartsWith('Get-WinEvent') })
if ($eventBlock.Count -ne 1) { throw 'Expected one process-event recipe.' }
function Get-WinEvent {
    param($FilterHashtable)
    if ($FilterHashtable.Id -ne 4688) { throw 'Wrong event filter.' }
    $fakeEvent = [pscustomobject]@{}
    $fakeEvent | Add-Member -MemberType ScriptMethod -Name ToXml -Value {
        '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event"><System><TimeCreated SystemTime="2026-10-25T03:04:05Z"/></System><EventData><Data Name="NewProcessName">C:\Temp\runner.exe</Data><Data Name="CommandLine">C:\Temp\runner.exe --mode audit</Data></EventData></Event>'
    }
    $fakeEvent
}
$rendered = & ([scriptblock]::Create($eventBlock[0].Groups[1].Value)) | Out-String
foreach ($value in @('2026-10-25T03:04:05Z', 'C:\Temp\runner.exe', 'C:\Temp\runner.exe --mode audit')) {
    if (-not $rendered.Contains($value)) { throw "Missing named field value: $value" }
}
'PowerShell syntax and named-field mapping passed; real EVTX ingestion was not tested.'
