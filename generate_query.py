from __future__ import division
from pymongo import MongoClient
import sys
import getopt
import random
import time

def usage():
	print "To be defined.."



def main():

	database = "musicbrainz2"
	collection = "records4"
	loop = 5000
	limit = 100
	text = False
	wordFile = ""
	artistFile = ""
	albumFile = ""
	recordingFile = ""
	millis = 0
	loopMillis = 0
	nscanned = 0
	loopNscanned = 0
	n = 0
	loopN = 0
	queryList = []
	queries = 0
	loopQueries = 0
	last_time = 0
	first_time = 0

	try:
		opts, args = getopt.getopt(sys.argv[1:], 
			"d:c:l:p:w:a:b:r:th", 
			["db","collection","limit","loop","wordfile","artistfile","albumfile","recordingfile","text","help"])
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(1)



	for o, a in opts:
		if o in ("-d", "--db"):
			database = a
		elif o in ("-c", "--collection"):
			collection = a
		elif o in ("-l", "--limit"):
			limit = int(a)
		elif o in ("-p", "--loop"):
			loop = int(a)
		elif o in ("-w", "--wordfile"):
			wordFile = a
		elif o in ("-a", "--artistfile"):
			artistFile = a
		elif o in ("-b", "--albumfile"):
			albumFile = a
		elif o in ("-r", "--recordingfile"):
			recordingFile = a
		elif o in ("-t", "--text"):
			text = True
		elif o in ("-h", "--help"):
			usage()
			sys.exit()
		else:
			usage()
			sys.exit(2)

	try:
		connection = MongoClient()
		db = connection[database]
		recording=db[collection]

	except:
		print "PyMongo - Unexpected error:", sys.exc_info()[0]
		sys.exit(3)

	

	if text:
			try:
				for word in open(wordFile, 'r').read().split('\n'):
					if word:
						loopQueries += 1
						queryList.append(word)
			except:
				print "Unable to process wordfile: "+wordFile+" word: <"+word+">"
				sys.exit(4)
	else:

			try:
				for artist in open(artistFile, 'r').read().split('\n'):
					query = {}
					if artist:
						query['artist'] = artist
						queryList.append(query)
			except:
				print "Unable to process artistfile: "+artistFile
				sys.exit(5)
			try:
				for album in open(albumFile, 'r').read().split('\n'):
					query = {}
					if album:
						query['album'] = album
						queryList.append(query)
			except:
				print "Unable to process albumfile: "+albumFile
				sys.exit(6)
			try:
				for name in open(recordingFile, 'r').read().split('\n'):
					query = {}
					if name:
						query['name'] = name
						queryList.append(query)
			except:
				print "Unable to process recordingfile: "+recordingFile
				sys.exit(7)




	first_time = time.time()
	last_time = first_time
	for i in range(0,loop):
		loopQueries = 0
		loopMillis = 0
		loopNscanned = 0
		loopN = 0
		if text:
			try:
				for word in queryList:
					loopQueries += 1
					#print "word: <"+word+">"
					a = db.command("text", collection, search=word, limit=limit)
					loopMillis += int(a['stats']['timeMicros']/1000)
					loopNscanned += a['stats']['nscanned']
					loopN += a['stats']['n']
					#a = db.command('text', collection, search=word)
					#a = recording.find({'$text': {'$search': word}}).limit(limit).explain()
					#millis += a['millis']
			except:
				print "Query - Unexpected error:", sys.exc_info()[0]
				sys.exit(4)

		else:
			random.shuffle(queryList)
			#print queryList
			for query in queryList:
				#print query
				try:
					loopQueries += 1
					a = recording.find(query).explain()
					loopNscanned += a['nscanned']
					loopN += a['n']
					loopMillis += a['millis']
				except:
					print "Query - Unexpected error:", sys.exc_info()[0]

		print str(int(time.time()-last_time))+": queries: "+str(loopQueries)+" loop: "+str(i)+" scanned: "+str(loopNscanned)+" matched: "+str(loopN)+" millis: "+str(loopMillis)+" avg(microsec): "+str(int(loopNscanned/loopMillis*1000))
		last_time = time.time()
		queries += loopQueries
		nscanned += loopNscanned
		n += loopN
		millis += loopMillis


	print str(int(time.time()-first_time))+": total queries: "+str(queries)+" loops: "+str(loop)+" scanned: "+str(nscanned)+" matched: "+str(n)+" millis: "+str(millis)+" avg(microsec): "+str(int(nscanned/millis*1000))

if __name__ == "__main__":
	main()
