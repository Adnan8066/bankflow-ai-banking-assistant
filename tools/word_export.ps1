# Export a DOCX to PDF with Microsoft Word and record the page number of every
# Heading 1 (used to build an accurate contents page in the BankFlow guide).
param(
    [Parameter(Mandatory = $true)][string]$Docx,
    [Parameter(Mandatory = $true)][string]$Pdf,
    [string]$PageMapJson = ""
)

$ErrorActionPreference = "Stop"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

$doc = $null
try {
    $doc = $word.Documents.Open($Docx, $false, $true)

    if ($PageMapJson -ne "") {
        $map = [ordered]@{}
        $count = $doc.Paragraphs.Count
        for ($i = 1; $i -le $count; $i++) {
            $paragraph = $doc.Paragraphs.Item($i)
            $styleName = $paragraph.Style.NameLocal
            if ($styleName -notmatch '^Heading 1') { continue }  # "Heading 1" / "Heading 1,Heading 1"

            $text = ($paragraph.Range.Text -replace "`r", "" -replace "`a", "").Trim()
            if ($text -eq "") { continue }

            $page = $paragraph.Range.Information(3)   # wdActiveEndPageNumber

            if ($text -match '^(Step|Lesson)\s+(\d+)\.') {
                $prefix = $Matches[1].ToLower()
                $map["$prefix$($Matches[2])"] = [int]$page
            }
            elseif ($text -match '^Appendix\s+([A-D])\.') {
                $map["appendix$($Matches[1].ToLower())"] = [int]$page
            }
            elseif ($text -match '^Contents$') {
                $map["contents"] = [int]$page
            }
        }
        ($map | ConvertTo-Json) | Set-Content -LiteralPath $PageMapJson -Encoding UTF8
        Write-Output "Page map entries: $($map.Keys.Count)"
    }

    $doc.ExportAsFixedFormat($Pdf, 17)   # wdExportFormatPDF
    Write-Output "PDF pages: $($doc.ComputeStatistics(2))"   # wdStatisticPages
}
finally {
    if ($doc) { $doc.Close($false) }
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
