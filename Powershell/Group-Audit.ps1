# Powershell script to dump all AD groups and their members
# (Taken from another script and modified)

# Change this if necesssary
$DATE = Get-Date -Format dd-MM-yyyy
$OUTPUT = "C:\Users\matt\SecurityGroups-$DATE.csv"
Write-Host "[INFO] Importing module..."
Import-Module ActiveDirectory

$Groups = (Get-AdGroup -filter * | Where {$_.name -like "**"} | select name -ExpandProperty name)

$Table = @()

$Record = @{
  "Group Name" = ""
  "Name" = ""
  "Username" = ""
}

Write-Host "[INFO] Digging through AD..."
Foreach ($Group in $Groups) {

  $Arrayofmembers = Get-ADGroupMember -identity $Group -recursive | select name,samaccountname

  foreach ($Member in $Arrayofmembers) {
    $Record."Group Name" = $Group
    $Record."Name" = $Member.name
    $Record."UserName" = $Member.samaccountname
    $objRecord = New-Object PSObject -property $Record
    $Table += $objrecord

  }
}

Write-Host "[INFO] Writing output to file"
$Table | Export-Csv $OUTPUT -NoTypeInformation

Write-Host "[INFO] Complete."
