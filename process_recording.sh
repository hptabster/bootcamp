#!/bin/bash
. ./unquote.sh
for i in /tmp/recording_*
do
  echo "./process_one_recording.sh $i >> $i.log 2>&1 &"
  nohup ./process_one_recording.sh $i >> $i.log 2>&1 &
done
