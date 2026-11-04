param([string]$ArduinoCli = 'arduino-cli')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
python (Join-Path $PSScriptRoot 'refresh-firmware-data.py') --prepare
if ($LASTEXITCODE -ne 0) { throw 'Source preparation failed.' }
& $ArduinoCli core install arduino:avr@1.8.8
if ($LASTEXITCODE -ne 0) { throw 'Arduino AVR core installation failed.' }
foreach ($mode in @('original', 'candidate', 'frontpanel')) {
    $sketchPath = Join-Path $projectRoot ('simulation\firmware\' + $mode)
    $buildPath = Join-Path $projectRoot ('build\' + $mode)
    $includePath = $sketchPath.Replace('\', '/')
    & $ArduinoCli compile --fqbn arduino:avr:uno --build-path $buildPath --build-property ('compiler.cpp.extra_flags=-I' + $includePath) $sketchPath
    if ($LASTEXITCODE -ne 0) { throw ('Build failed: ' + $mode) }
    Copy-Item -LiteralPath (Join-Path $buildPath ($mode + '.ino.hex')) -Destination (Join-Path $projectRoot ('simulation\firmware\' + $mode + '.hex'))
    Copy-Item -LiteralPath (Join-Path $buildPath ($mode + '.ino.elf')) -Destination (Join-Path $projectRoot ('simulation\firmware\' + $mode + '.elf'))
}
python (Join-Path $PSScriptRoot 'refresh-firmware-data.py')
if ($LASTEXITCODE -ne 0) { throw 'Firmware metadata refresh failed.' }
python (Join-Path $PSScriptRoot 'build_workbench.py')
if ($LASTEXITCODE -ne 0) { throw 'Workbench generation failed.' }
Write-Output 'Rebuilt HEX/ELF, SRAM symbols and offline workbench.'
