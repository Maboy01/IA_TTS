$ErrorActionPreference = "Stop"

$rootPath = (Resolve-Path $PSScriptRoot).Path
$archivePath = Join-Path $rootPath "LJSpeech-1.1.tar.bz2"
$extractDir = Join-Path $rootPath "LJSpeech-1.1"
$dataRoot = Join-Path $rootPath "data"
$datasetDir = Join-Path $dataRoot "LJSpeech-1.1"
$metadataPath = Join-Path $datasetDir "metadata.csv"
$subsetPath = Join-Path $datasetDir "metadata_subset.csv"
$datasetUrl = "https://data.keithito.com/data/speech/LJSpeech-1.1.tar.bz2"

New-Item -ItemType Directory -Force -Path $dataRoot | Out-Null

if (-not (Test-Path -LiteralPath $archivePath)) {
    Write-Host "Descargando LJSpeech..."
    Invoke-WebRequest -Uri $datasetUrl -OutFile $archivePath
} else {
    Write-Host "Archivo ya descargado: $archivePath"
}

if (-not (Test-Path -LiteralPath $datasetDir)) {
    Write-Host "Extrayendo dataset..."
    tar -xf $archivePath -C $rootPath

    if (-not (Test-Path -LiteralPath $extractDir)) {
        throw "No se encontro la carpeta extraida esperada: $extractDir"
    }

    New-Item -ItemType Directory -Force -Path $datasetDir | Out-Null
    Get-ChildItem -LiteralPath $extractDir | Move-Item -Destination $datasetDir
} else {
    Write-Host "Dataset ya preparado en: $datasetDir"
}

if (-not (Test-Path -LiteralPath $metadataPath)) {
    throw "No se encontro metadata.csv en: $metadataPath"
}

Get-Content -LiteralPath $metadataPath -TotalCount 200 | Set-Content -LiteralPath $subsetPath

Write-Host ""
Write-Host "Listo."
Write-Host "Dataset: $datasetDir"
Write-Host "Subset:  $subsetPath"
