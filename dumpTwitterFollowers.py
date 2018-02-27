#!/usr/bin/python3

import os
import gzip
import shutil
import logging.config
import argparse
import twitter
import sys
import traceback
import unicodecsv as csv
import datetime
import time

# own modules
from api import TweetRc
from util import toStr

# constants
SLEEP_ON_ERROR_MINS=5

# set up logging
logging.config.fileConfig('logging.conf')

def main():

	# parse args
	parser = argparse.ArgumentParser()
	parser.add_argument('-rc', '--tweetrc', help="tweetrc file for API auth")
	parser.add_argument('-ff', '--from-file', help="read screen names from file")
	parser.add_argument('-z', '--gzip', dest='gzip', action='store_true', help="run CSV output through gzip")
	parser.add_argument('usernames', metavar="screen_name", nargs='*', help="list of screen names")
	parser.set_defaults(gzip=False)
	args = parser.parse_args()
	rcPath = args.tweetrc

	# verify args
	if args.from_file:
		logging.info("Loading users to process from file: %s" % args.from_file)
		with open(args.from_file) as usersFile:
			users=[line.strip(' \n') for line in usersFile.readlines()]
	else:
		users = args.usernames 

	if not len(users):
		print("Please provide at least 1 screen name or file to process.")
		parser.print_help()
		sys.exit(1)

	logging.info("Number of users to process: %d" % len(users))

	# load list of fields/cols to extract
	with open("USER_FIELDS") as fieldsFile:
		fieldNames = [field.strip(' \n') for field in fieldsFile.readlines()]

	# load twitter user conf and api
	rc = TweetRc(rcPath)
	api = twitter.Api(consumer_key=rc.getConsumerKey(), consumer_secret=rc.getConsumerSecret(),
		access_token_key=rc.getAccessToken(), access_token_secret=rc.getAccessSecret(),
		sleep_on_rate_limit=True,input_encoding=None)
	logging.info("Connected to API and authorized.")

	# extract all given users' followers
	for username in users:
		logging.info("Dumping followers of %s" % username)
		# create CSV file (in utf-8, including BOM)
		nextCursor = -1
		csv_filename = "%s-%s.csv" % (username, datetime.datetime.now().strftime("%Y%m%d"))
		# write header and rows
		with open(csv_filename, 'wb') as csvFile:
			startT = time.time()
			numFollowers = 0
			logging.info("Writing to %s" % csv_filename)
			csvFile.write(u'\ufeff'.encode('utf8')) # BOM 
			follWriter = csv.DictWriter(csvFile, fieldNames, encoding='utf-8', delimiter = ',',
								quotechar='|', quoting=csv.QUOTE_MINIMAL)
			follWriter.writeheader()
			# fetch followers and dump to CSV
			while nextCursor != 0:
				try:
					nextCursor,prevCursor,followers = api.GetFollowersPaged(screen_name=username, cursor=nextCursor)
				except:
					traceback.print_exc(file=sys.stderr)
					logging.exception("Error obtaining next page of followers (w/ nextCursor=%d)" % nextCursor)
					time.sleep(SLEEP_ON_ERROR_MINS * 60)	
				else:
					for u in followers:
						newRow = {fld: toStr(getattr(u,fld)) for fld in fieldNames}
						follWriter.writerow(newRow)
						numFollowers+=1
			endT = time.time()
			logging.info("%d followers of %s dumped to %s in %f" % (numFollowers, username, csv_filename, endT - startT))

		# (optionally) gzip and delete CSV file
		if args.gzip:
			with open(csv_filename, 'rb') as csvFile:
				gz_filename = csv_filename+'.gz'
				with gzip.open(gz_filename,'wb') as gzFile:
					shutil.copyfileobj(csvFile, gzFile)
					logging.info("CSV compressed to %s" % gz_filename)
			os.remove(csv_filename)
			logging.info("Plain file %s deleted" % csv_filename)

if __name__=="__main__":
	main()
