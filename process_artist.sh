#!/bin/bash
p=`pwd`
pushd /tmp
split -l 20000 $p/artist_credit /tmp/artist_credit_
popd
for i in /tmp/artist_credit_[a-Z]*
do
  echo "./process_one_artist.sh $i >> $i.log 2>&1 &"
  nohup ./process_one_artist.sh $i >> $i.log 2>&1 &
done
