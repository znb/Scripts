# Simple script to generate a decent password and copy to clipboard

param( 
[int] $len = 15,  # Adjust this if required
[string] $chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_!@#$%^&*()_"
)

Write-Output "Generating Password with length: $len"
$bytes = new-object "System.Byte[]" $len
$rnd = new-object System.Security.Cryptography.RNGCryptoServiceProvider
$rnd.GetBytes($bytes)
$result = ""

for( $i=0; $i -lt $len; $i++ )
{
$result += $chars[ $bytes[$i] % $chars.Length ]	
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
