#!/bin/bash
#p=`pwd`
#pushd /tmp
#split -l 100000 $p/track /tmp/track_
#popd
for i in /tmp/track_[a-z][a-z]
do
  echo "./process_one_track.sh $i >> $i.log 2>&1 &"
  nohup ./process_one_track.sh $i >> $i.log 2>&1 &
done
