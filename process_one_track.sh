#!/bin/bash
echo "`date`: Loading $1"
python musicbrainz2_denormalize-lower.py $1
echo "`date`: Completed $1"
