#!/bin/bash
IFS="	"
. ./unquote.sh
echo "`date`: Reading $1"
while read id gid name rest
do
   name2=`unquote $name`
   echo "db.recording.update({release_id: $id},{\$set: {release_name: '$name2'}},{multi:true})"
done < $1 > $1.js
echo "`date`: Loading $1"
mongo localhost/musicbrainz < $1.js
echo "`date`: Completed $1"
