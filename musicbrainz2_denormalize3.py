import pymongo
import sys
import csv
import time
import hashlib
import pickle

track_tsv = sys.argv[1]
connection = pymongo.Connection("mongodb://54.225.100.39", safe=True)

db = connection.musicbrainz2
recording = db.recording
artist = db.artist_credit
release = db.release
medium = db.medium
records = db.records3

with open(track_tsv,'rb') as tracks:
    tracks = csv.reader(tracks, delimiter='\t')

    i = 0
    i_rec = 0
    bulk_rec = []
    last_rec = {}
    first_time = time.time()
    last_time = first_time
    for track in tracks:
	#track="_id,gid,recording_id,medium_id,pos,num,name,artist_credit_id,length,edits,last_update"
	i += 1
	rec = {}
	res = {}
	rec['_id'] = 0
	med_id = int(track[3])
	art_id = int(track[7])
	rec['name'] = track[6]
	rec['length'] = int(track[7])
	rec['artist'] = artist.find_one({"_id": art_id})['name']
	rec['pos'] = track[4]
	rel_id = medium.find_one({"_id": med_id})['release_id']
	rec['album'] = release.find_one({"_id": rel_id})['name']
	#print "------"
	#print rec
	#print last_rec
	#print
	if rec != last_rec:
		#rec['_id'] = track[0]
		#print rec
		#u = rec['name'].encode('base64')+str(rec['length'])+rec['artist'].encode('base64')+str(rec['pos'])+rec['album'].encode('base64')
		rec['_id'] = hashlib.md5(pickle.dumps(rec)).hexdigest()
		#print "new rec"
		#print rec
		bulk_rec.append(rec.copy())
		#print bulk_rec
		#print "-------"
		i_rec += 1
		if (i_rec % 1000) == 0:
			#print bulk_rec
			try:
			    records.insert(bulk_rec, continue_on_error=True)
			except:
			    print "Recording - Unexpected error:", sys.exc_info()[0]
			bulk_rec = []
			print str(int(time.time()-last_time))+": "+str(i_rec)
			last_time = time.time()
	last_rec = rec
	last_rec['_id'] = 0

if len(bulk_rec) > 0:
    try:
	records.insert(bulk_rec, continue_on_error=True)
    except:
	print "Recording - Unexpected error:", sys.exc_info()[0]

print "File: "+track_tsv+" - Total records: "+str(i)+" inserted records: "+str(i_rec)+" total time: "+str(int(time.time()-first_time))
