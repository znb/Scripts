#!/bin/bash

# Very simple web shell finder
# from here http://pentestlab.org/hunting-malicious-perl-irc-bots/

PATH=$1

echo "Scanning $PATH"
echo -n "Scanning for "
echo -n "tcp, "
/bin/grep -Rn "tcp *(" $PATH
echo -n "system, "
/bin/grep -Rn "system *(" $PATH
echo -n "shell."
/bin/grep -Rn "shell *(" $PATH
echo -n "shell_exec."
/bin/grep -Rn “shell_exec *(” $PATH
echo -n "base64_decode."
/bin/grep -Rn “base64_decode *(” $PATH
echo -n "phpinfo."
/bin/grep -Rn “phpinfo *(” $PATH
echo -n "php_uname."
/bin/grep -Rn “php_uname *(” $PATH
echo -n "chmod."
/bin/grep -Rn “chmod *(” $PATH
echo -n "fopen."
/bin/grep -Rn “fopen *(” $PATH
echo -n "fclose."
/bin/grep -Rn “fclose *(” $PATH
echo -n "readfile."
/bin/grep -Rn “readfile *(” $PATH
echo -n "edoced_46esab."
/bin/grep -Rn “edoced_46esab *(” $PATH
echo -n "eval."
/bin/grep -Rn “eval *(” $PATH
echo -n "passthru."
/bin/grep -Rn “passthru *(” $PATH

echo "We're done here"
