time mongoimport -f "_id,gid,name,artist_id,length,comment,edits,update" --type tsv -d musicbrainz2 -c recording recording
time mongoimport -f "_id,name,artist_count,ref_count,created" --type tsv -d musicbrainz2 -c artist_credit artist_credit
time mongoimport -f "_id,gid,recording_id,medium_id,pos,num,name,artist_credit_id,length,edits,last_update" --type tsv -d musicbrainz2 -c track track
time mongoimport -f "_id,gid,name,rest" --type tsv -d musicbrainz2 -c release release
time mongoimport -f "_id,release_id,pos,format,name,edits,last_update,track_count" --type tsv -d musicbrainz2 -c medium medium
