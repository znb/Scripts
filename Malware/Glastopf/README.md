If you're not using [Glastopf](https://github.com/glastopf/glastopf) as your web honeypot, you
might be doing something wrong.

These are just some scripts I pulled together to look at the log file


glastopf-report.sh
------------------

Just a quick and dirty bash script to pull useful info from your Glastopf log file.

Usage: 

```
 ./glastopf-report.sh /path/to/your/glastopf.log
```

Useful stuff in the report:

 * Total sessions
 * Offenders
 * Requested URLs

glastopfdb-query.py
-------------------

A simple script to query the Glastopf database and return useful information

Usage: 

```
./glastopfdb-query.py -d /path/to/your/glastopf.db [-a] [-s attackerip] [-i attackid] [-l] [-S]
```

Useful stuff in the report:

 * Dump all entries in the database
 * Show a specific attack ID
 * Search for a specific attacker
 * List all attackers in the database (with number of attacks and attack IDs)
 * Summary report for the database (Not quite done)
 
