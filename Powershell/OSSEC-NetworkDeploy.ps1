# Deploy OSSEC from a network share

param(
        [string]$clientid = $args[1]
)

$ossecinstaller = "ossec-win32-agent-2.8.3.exe"
$ossecshare = "\\192.168.1.1\OSSEC"
$ossecsrc = "\Installer"
$osseccfg = "\Configs"
$ossecdst = "C:\Temp"


function Am-I-Admin {
    $identity = [System.Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = new-object System.Security.Principal.WindowsPrincipal($identity)
    $admin = [System.Security.Principal.WindowsBuiltInRole]::Administrator
    $principal.IsInRole($admin)
}


function Map-Drive{

    "[INFO] Mapping network drive"
    try {
        $mount = (New-Object -Com WScript.Network).MapNetworkDrive("o:", $ossecshare)
    }
    catch {
        Write-Warning "Something has gone horriby wrong"
    }
}


function Copy-Installer {

    if (!(Test-Path -path $ossecdst))
    {
        New-Item $ossecdst -type directory | Out-Null
    }

    "[INFO] Copying Installer"
    Copy-Item "o:\$ossecsrc\$ossecinstaller" $ossecdst
    "[INFO] Copying Configs"
    Copy-Item "o:\$osseccfg\$clientid.zip" $ossecdst
}


function OSSEC-Install {
    "[INFO] Installing OSSEC Quietly"
    $install = Start-Process -FilePath $ossecinstaller -WorkingDirectory $ossecdst -ArgumentList '/S'
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
    "[INFO] OSSEC Configuration"
    "[INFO] Removing default configuration"
    try {
        Remove-Item "C:\Program Files (x86)\ossec-agent\client.keys" -ErrorAction Continue | Out-Null
    }
    catch {
        # TODO: Better way to do this ?
    }
    try {
        Remove-Item "C:\Program Files (x86)\ossec-agent\ossec.conf" -ErrorAction Continue | Out-Null
    }
    catch {
        # TODO: Better way to do this ?
    }

    try {
        "[INFO] Extracting config: $clientid"
        Extract-Config -File "$ossecdst\$clientid.zip" -Destination "C:\Program Files (x86)\ossec-agent"
    }
    catch {
        Write-Warning "Wrong Client ID used."
        Exit
    }
}


function OSSEC-Start {
    "[INFO] Starting OSSEC"
    "[INFO] Sleeping 5secs before starting service"
    Start-Sleep -s 5
    try {
        Start-Service OssecSvc
    }
    catch {
        Write-Warning "Something has gone horribly wrong"
    }
}


function Cleanup {
    try {
        "[INFO] Unmapping drive..."
        (New-Object -Com WScript.Network).RemoveNetworkDrive("o:")
    }
    catch {
        Write-Warning "Error unmapping drive."
    }
    try {
        Remove-Item "$ossecdst\$ossecinstaller" -ErrorAction Stop
        Remove-Item "$ossecdst\$clientid.zip" -ErrorAction Stop
    }
    catch {
        Write-Warning "Clean up failed"
    }
}


# Get this party started
if (!(Am-I-Admin)) {
    Write-Warning "Not running as administrator"
    Exit
}
else {
    "[INFO] Starting deployment of OSSEC..."
    Map-Drive
    Copy-Installer
    OSSEC-Install
    OSSEC-Config
    OSSEC-Start
    Cleanup
    "`n[INFO] Install Complete."
}
