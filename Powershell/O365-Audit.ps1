# Powershell script to dump all Office365 Users

# Change this if necesssary
$DATE = Get-Date -Format dd-MM-yyyy
$LOUTPUT = "C:\Users\matt\Licensed-O365-Audit-$DATE.csv"

Import-Module MSOnline

Write-Host "[INFO] Connecting to O365"
Connect-MsolService

Write-Host "[INFO] Pulling data from O365"
Get-MsolUser | Where-Object { $_.isLicensed -eq "True" } | Select-Object UserPrincipalName, DisplayName, Country, Department | Export-Csv $LOUTPUT
Write-Host "[INFO] Writing output"
Write-Host "[INFO] Complete"
