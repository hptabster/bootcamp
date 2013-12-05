#/bin/bash

_usage_()
{
cat << EOF
usage: $0 options
   -l <limit>, default $limit
   -p <loop num>, default $loop
   -d <db>, default $db
   -c <collection>, default $collection
   -t <0,1>, text search, default $text
EOF
_cleanup_ 1
}


_cleanup_()
{
   rm -f $js $unsort_words $unsort_albums* $unsort_artists* $unsort_recordings*
   exit $1
}

unquote()
{
  echo $1 | sed -e "s.\".\\\\\".g"
}

get_numrecs()
{
   echo `wc -l $1 | sed -e 's,^ *,,;s, .*,,'`
}

#albums=/data/tmp/albums.txt
#artists=/data/tmp/artists.txt
#recordings=/data/tmp/recordings.txt
albums=/data/tmp/albums-unsort.txt
artists=/data/tmp/artists-unsort.txt
recordings=/data/tmp/recordings-unsort.txt
#unsort_albums=/tmp/albums.$$
#unsort_artists=/tmp/artists.$$
#unsort_recordings=/tmp/recordings.$$
words=/data/tmp/words.txt
js=/tmp/$$.js
unsort_words=/tmp/words-unsort.$$
unsort_albums=/tmp/albums-unsort.$$
unsort_artists=/tmp/artists-unsort.$$
unsort_recordings=/tmp/recordings-unsort.$$

loop=5000
limit=100
collection=records4
db=musicbrainz2
text=0
text_limit=100

# Main Program
trap _cleanup_ SIGINT SIGTERM

# Process command line arguments
while getopts "c:d:l:p:t:" flag
do
   case $flag in
     c)
        collection="$OPTARG"
        ;;
     d)
        db="$OPTARG"
        ;;
     l)
        limit="$OPTARG"
        ;;
     p)
        loop="$OPTARG"
        ;;
     t)
        text="$OPTARG"
        ;;
     *)
        _usage_
        ;;
   esac
done

if [ $text -eq 1 ]; then
   num_words=`get_numrecs $words`
   tail -n +$((RANDOM % (num_words-limit))) $words | head -n$limit > $unsort_words
   #cat $unsort_words
   python generate_query.py -d $db -c $collection -t -w $unsort_words -l $limit -p $loop
else
   num_albums=`get_numrecs $albums`
   num_artists=`get_numrecs $artists`
   num_recordings=`get_numrecs $recordings`
   tail -n +$((RANDOM % (num_albums-limit))) $albums | head -n$limit > $unsort_albums
   tail -n +$((RANDOM % (num_artists-limit))) $artists | head -n$limit > $unsort_artists
   tail -n +$((RANDOM % (num_recordings-limit))) $recordings | head -n$limit > $unsort_recordings

   python generate_query.py  -d $db -c $collection -a $unsort_artists -b $unsort_albums -r $unsort_recordings  -l $limit -p $loop

fi

_cleanup_ 0
