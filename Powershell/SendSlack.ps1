Function Send-Slack
{

  Param(
   [parameter(Mandatory=$true)]
   [String]
   $SlackString
  )

  $SlackWebHook = 'https://hooks.slack.com/services/LOLS/KTHXBIBBQWTF/Bieber'
  $SlackData = @{text = $SlackString}
  $SlackPayload = ConvertTo-Json $SlackData
  Write-Host "Sending Slack message..."
  Invoke-WebRequest -Uri $SlackWebHook -TimeoutSec 5 -Method POST -Body $SlackPayload | Out-Null
}
Export-ModuleMember -Function Send-Slack
