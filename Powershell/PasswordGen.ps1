# Simple script to generate a decent password and copy to clipboard

param( 
[string] $length = 15,
[string] $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_!@#$%^&*()_"
)

Write-Output "Generating Password with length: $length"
if ($length -le "10") {
Write-Output "[WARNING] Passwords less than 10 caracters are considered weak"
}

$bytes = new-object "System.Byte[]" $length
$rnd = new-object System.Security.Cryptography.RNGCryptoServiceProvider
$rnd.GetBytes($bytes)
$result = ""

for( $i=0; $i -lt $length; $i++ )
{
$result += $chars[ $bytes[$i] % $chars.length ]	
}

# This copies stuff to the clipboard
function To-Clipboard {

$null = [Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms")
$dataObject = New-Object windows.forms.dataobject
$dataObject.SetData([Windows.Forms.DataFormats]::UnicodeText, $true, $result)
[Windows.Forms.Clipboard]::SetDataObject($dataObject, $true)
}

To-Clipboard
Write-Output "`r`nPassword copied to clipboard`r`n"
Write-Output "Password: $result"
