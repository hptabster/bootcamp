#!/bin/bash
#IFS="	"
#. ./unquote.sh
#echo "`date`: Reading $1"
#while read id gid name rest
#do
   #name2=`unquote $name`
   #echo "db.track.update({recording: $id},{\$set: {recording_name: '$name2'}},{multi:true})"
#done < $1 > $1.js
echo "`date`: Loading $1"
mongo localhost/musicbrainz < $1.js
echo "`date`: Completed $1"
