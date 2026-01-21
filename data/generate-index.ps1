# data 폴더에서 실행하세요
# PowerShell: .\generate-index.ps1

$files = Get-ChildItem -Name *.csv | Sort-Object
$json = $files | ConvertTo-Json
$json | Out-File -FilePath "index.json" -Encoding UTF8
Write-Host "index.json 생성 완료! ($($files.Count)개 파일)"
