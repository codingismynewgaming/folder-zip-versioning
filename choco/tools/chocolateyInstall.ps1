$ErrorActionPreference = 'Stop'

$packageName = 'folderzipper-versioning'
$softwareName = 'FolderZipperVersioning'
$installerType = 'EXE'
$silentArgs   = '/VERYSILENT'
$validExitCodes = @(0)

$version = '1.2.0'
$url = "https://github.com/codingismynewgaming/folder-zip-versioning/releases/download/v1.2/FolderZipperVersioning.exe"

# Get SHA256 hash dynamically
$checksum = (Get-FileHash -Uri $url -Algorithm SHA256).Hash

Install-ChocolateyPackage `
  -PackageName $packageName `
  -FileType $installerType `
  -SilentArgs $silentArgs `
  -ValidExitCodes $validExitCodes `
  -Url $url `
  -Checksum $checksum `
  -ChecksumType 'sha256'
