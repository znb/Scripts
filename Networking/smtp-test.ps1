$CREDENTIALS = Get-Credential

Send-MailMessage –From italerts@example.com –To user@example.com –Subject “Test Email” –Body “Test SMTP Relay Service” -SmtpServer smtp.office365.com -Credential $CREDENTIALS -UseSsl -Port 587
