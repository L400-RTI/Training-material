# Set the directory containing the Markdown files
$sourceDirectory = "./modules"

# Set the output file path
$outputFile = "./workshop.md"

# Optional: file ordering (use Get-ChildItem -Name | Sort-Object if alphabetical)
$markdownFiles = Get-ChildItem -Path $sourceDirectory -Filter "*.md" | Sort-Object Name

# Clear the output file if it exists
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}

# Combine files
foreach ($file in $markdownFiles) {
    Write-Host "Adding $($file.Name) to output..."
    Get-Content -Path $file.FullName | `
        ForEach-Object {
            $_ -replace "/assets/", "/modules/assets/"
        } | `
            Add-Content -Path $outputFile
}

Write-Host "Combined $($markdownFiles.Count) files into $outputFile"