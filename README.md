# Mozilla RSS Feed Monitor

## Summary

Parse each RSS feed in a list for specific terms that we care about
and send notification email to a list of recipients when term matches
are found.

## Details

The single Python script, `scripts/feedMonitor.py`, can be run as a
cron job.  As it finds term matches, it records them in a database
table to avoid sending duplicate alerts in the future.  The schema for
this table can be found in `data/table.sql`.
