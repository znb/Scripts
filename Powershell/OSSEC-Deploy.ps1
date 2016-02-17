# Simple script to download Wuzah OSSEC and
# deploy with client config and key

param(
        [string]$clientid = $args[1]
)

$dstdir = "C:\Temp"
$ossecexe = "ossec-install.exe"
$downloadurl = "http://ossec.wazuh.com/windows/ossec-win32-agent-2.8.3.exe"
$goodhash = "4ebcb31e4eccd509ae34148dd7b1b78d75b58f53"


function Am-I-Admin {
    $identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = new-object System.Security.Principal.WindowsPrincipal($identity)
    $admin = [System.Security.Principal.WindowsBuiltInRole]::Administrator
    $principal.IsInRole($admin)
}


function OSSEC-Download {

    "`n[INFO] Downloading OSSEC"

    "Source: [$downloadurl]"
    "`nDestination: [$dstdir\$ossecexe]"

    "Checking destination directory: $dstdir"
    if (!(Test-Path -path $dstdir))
    {
        New-Item $dstdir -type directory | Out-Null
    }

    try {
        Invoke-WebRequest $downloadurl -OutFile $dstdir\$ossecexe
    }
    catch [System.IO.DirectoryNotFoundException],[System.IO.DirectoryNotFoundException] {
        "`n[ERROR] Unable to download file !!"
    }

    $filehash = (Get-FileHash -Algorithm SHA1 -Path $dstdir\$ossecexe).Hash

    if ($goodhash -ne $filehash) {
        Write-Warning "[ERROR] Hashes don't match !!"
        Remove-Item $dstdir\$ossecexe
        Exit
    }
}


function OSSEC-Install {
    "`n[INFO] Installing OSSEC Quietly"
    $install = Start-Process -FilePath $ossecexe -WorkingDirectory $dstdir -ArgumentList '/S'
}

function Extract-Config($file, $destination) {

    $shell = New-Object -com shell.application
    $zip = $shell.NameSpace($file)
    foreach($item in $zip.items())
    {
        $shell.Namespace($destination).copyhere($item)
    }
}


function OSSEC-Config {
    "`n[INFO] Dropping in OSSEC Config"
    "[INFO] Removing default configuration"
    try {
        Remove-Item "C:\Program Files (x86)\ossec-agent\client.keys" -ErrorAction Stop
    }
    catch {
        Write-Warning "OSSEC Client key"
    }
    try {
        Remove-Item "C:\Program Files (x86)\ossec-agent\ossec.conf" -ErrorAction Stop
    }
    catch {
        Write-Warning "OSSEC Config file"
    }

    try {
        "[INFO] Extracting config: $clientid"
        Extract-Config -File "$dstdir\$clientid.zip" -Destination "C:\Program Files (x86)\ossec-agent"
    }
    catch {
        Write-Warning "Wrong Client ID used."
        Exit
    }
}

function OSSEC-Start {
    "`n[INFO] Starting OSSEC"
    "[INFO] Sleeping 5secs before startin service"
    Start-Sleep -s 5
    try {
        Start-Service OssecSvc
    }
    catch {
        Write-Warning "Something has gone horribly wrong"
    }
}


function Cleanup {
    "`n[INFO] Clean up"
    try {
        Remove-Item $dstdir/$ossecexe -ErrorAction Stop
    }
    catch {
        Write-Warning "Clean up..."
    }
}


if (!(Am-I-Admin)) {
    Write-Warning "Not running as administrator"
    Exit
}
else {
    OSSEC-Download
    OSSEC-Install
    OSSEC-Config
    OSSEC-Start
    Cleanup
}
