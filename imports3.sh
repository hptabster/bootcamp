tables="recording artist_credit track release medium"
db=musicbrainz3
for i in $tables
do
   fields=`grep $i= fields.txt | cut -f2 -d "="`
   echo "time mongoimport -f $fields --type tsv -d $db -c $i $i"
done
