import pymongo
import sys
import time

connection = pymongo.Connection("mongodb://54.225.100.39", safe=True)

db = connection.musicbrainz2
recording = db.recording
artist = db.artist_credit
track = db.track
release = db.release
medium = db.medium
records = db.records

query = {}

try:
	iter = track.find(timeout=False)

except:
	print "Recording - Unexpected error:", sys.exc_info()[0]

i = 0
i_rec = 0
bulk_rec = []
last_rec = {}
last_time = time.time()
for record in iter:
	i += 1
	rec = {}
	rec['_id'] = 0
	med_id = record['medium_id']
	art_id = record['artist_credit_id']
	rec['name'] = record['name']
	rec['length'] = record['length']
	#rec['artist'] = artist.find_one({"_id": art_id},{"_id": 0, "name": 1})['name']
	rec['artist'] = artist.find_one({"_id": art_id})['name']
	rec['pos'] = record['pos']
	rel_id = medium.find_one({"_id": med_id})['release_id']
	rec['album_name'] = release.find_one({"_id": rel_id})['name']
	#print "------"
	#print rec
	#print last_rec
	#print
	if rec != last_rec:
		rec['_id'] = record['_id']
		#print "new rec"
		#print record
		#print rec
		bulk_rec.append(rec.copy())
		#print bulk_rec
		#print "-------"
		i_rec += 1
		if (i_rec % 1000) == 0:
			#print bulk_rec
			records.insert(bulk_rec)
			bulk_rec = []
			print str(int(time.time()-last_time))+": "+str(i_rec)
			last_time = time.time()
	last_rec = rec
	last_rec['_id'] = 0

if len(bulk_rec) > 0:
	records.insert(bulk_rec)

print "Total records: "+str(i)+" inserted records: "+str(i_rec)
