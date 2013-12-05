#!/bin/bash
IFS="	"
. ./unquote.sh
echo "`date`: Reading $1"
#while read id name rest
#do
   #name2=`unquote $name`
   #echo "db.recording.update({artist_id: $id},{\$unset :{gid:\"\",comments:\"\",edits\"\",update:\"\",field8:\"\"}, \$set: {artist_name: '$name2'}},{multi:true})"
#done < $1 > $1.js
echo "`date`: Loading $1"
mongo localhost/musicbrainz < $1.js
echo "`date`: Completed $1"
