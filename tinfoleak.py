#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import tweepy
import sys
import getopt
import datetime
import urllib2
import os
import string


# OAuth Settings
# How to obtain the API key:
# Go to https://dev.twitter.com/apps/new
# Copy the consumer key (API key), consumer secret, access token and access token secret
CONSUMER_KEY = '' 
CONSUMER_SECRET = '' 
ACCESS_TOKEN = '' 
ACCESS_TOKEN_SECRET = '' 


# App parameters (please, don't modify these values!)
program_name = "tinfoleak"
program_version = "v1.2"
program_date = "03/02/2014"
program_author_name = "Vicente Aguilera Diaz"
program_author_twitter = "@VAguileraDiaz"
program_author_companyname = "Internet Security Auditors"

# Global parameters
arg_name = "" # twitter account
arg_count = 100 # number of tweets to be analyzed
arg_time = 0 # 1 = show the time in the results, 0 = don't show the time in the results
arg_basic = 0 # 1 = show basic info for the user, 0 = don't show basic info for the user
arg_source = 0 # 1 = show the application used by the user, 0 = don't show the application used by the user
arg_hashtags = 0 # 1 = show the hashtags, 0 = don't show the hashtags
arg_mentions = 0 # 1 = show the user mentions, 0 = don't show the user mentions
arg_find = "" # word to search in the user timeline
arg_stime = "00:00:00" # start time (filter)
arg_etime = "23:59:59" # end time (filter)
arg_sdate = "1900/01/01" # start date (filter)
arg_edate = "2100/01/01" # end date (filter)
arg_output = "" # log file
arg_geofile = "" # KML file (Google Earth tweets visualization)
arg_pics = "" # directory to download user pictures
tweet_images = [] # store the user images
source = [] # store the applications (twitter client)
hashtags = [] # store the hashtags
user_mentions = [] # store the user mentions
tweet_with_word = [] # store the tweets filtered by the specified word
geo_info = [] # store the geolocation info
sdate = datetime.datetime.now() # the current date and time
color = "[1;96m" # color used in the headers

# User authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Tweepy (a Python library for accessing the Twitter API)
api = tweepy.API(auth)


################
# Print data to the console and log file
################
def print_data(data):
	try:
		print data
		if arg_output:
			tmp = filter(lambda x: x in string.printable, data)
			newdata = tmp.replace(color, " ").replace("[0m", " ")
			fd.write(newdata + "\n")
		
	except Exception, e:
		print "\n[ print_data() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Show credits
################
def show_credits():
	try:
		print "+++ "
		print "+++ " + program_name + " " + program_version + " - \"Get detailed information about a Twitter user\""
		print "+++ " + program_author_name + ". " + program_author_twitter
		print "+++ " + program_author_companyname
		print "+++ " + program_date
		print "+++ "
		print 

	except Exception, e:
		print "\n[ show_credits() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Show usage
################
def show_usage():
	try:
		print "Usage:\n# " + sys.argv[0] + " [-n|--name] username [-c|--count] count [-t|--time] [-b|--basic] [-s|--source] [-h|--hashtags] [-m|--mentions] [-g|--geo] geofile [--stime] stime [--etime] etime [--sdate] sdate [--edate] edate [-f|--find] word [-p|--pics] images [-o|--output] file"
		print "\t(*) username: Twitter account"
		print "\t    count: number of tweets to analyze (default value: 100)"
		print "\t    time: show time in every result (default value: off)"
		print "\t(+) basic: show basic information about the username (default value: off)"
		print "\t(+) source: show applications used by username (default value: off)"
		print "\t(+) hashtags: show hashtags used by username (default value: off)"
		print "\t(+) mentions: show twitter accounts used by username (default value: off)"
		print "\t(+) geofile: show geolocation information and save the results in KML format for Google Earth visualization (default value: off)"
		print "\t    stime: filter tweets from this start time. Format: HH:MM:SS (default value: 00:00:00)"
		print "\t    etime: filter tweets from this end time. Format: HH:MM:SS (default value: 23:59:59)"
		print "\t    sdate: filter tweets from this start date. Format: YYYY/MM/DD (default value: 1900/01/01)"
		print "\t    edate: filter tweets from this end date. Format: YYYY/MM/DD (default value: 2100/01/01)"
		print "\t(+) word: filter tweets that include this word"
		print "\t(x) images: [0] show images (parameter \"geofile\" is mandatory), [1] download images (to the \"screen_name\" directory)"
		print "\t    file: output file"
		print 
		print "\t(*) Required parameter"
		print "\t(+) One of these parameters must be informed"
		print "\t(x) If you enabled this option, you need to be patient. The execution time is greatly increased."
		print "\n\tExamples:"
		print "\t\t# " + sys.argv[0] + " -n vaguileradiaz -b"
		print "\t\t# " + sys.argv[0] + " -n stevewoz -sc 1000"
		print "\t\t# " + sys.argv[0] + " -n stevewoz -g stevewoz.kml -o output.log"
		print "\t\t# " + sys.argv[0] + " -n vaguileradiaz -thm"
		print "\t\t# " + sys.argv[0] + " -n billgates -g billgates.kml -p 1 -c 300"
		print "\t\t# " + sys.argv[0] + " -n vaguileradiaz -tc 500 -f secret --sdate 2013/10/01 -o output.log"
		print "\t\t# " + sys.argv[0] + " -n vaguileradiaz -shmtc 1000 --stime 08:00:00 --etime 18:00:00\n"

	except Exception, e:
		print "\n[ show_usage() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Get options
################
def get_options():
	global arg_name
	global arg_count
	global arg_time
	global arg_basic
	global arg_source
	global arg_hashtags
	global arg_mentions
	global arg_find
	global arg_stime
	global arg_etime
	global arg_sdate
	global arg_edate
	global arg_output
	global arg_geofile
	global arg_pics

	try:
		opts, args = getopt.getopt(sys.argv[1:], "n:c:tbshmg:f:p:o:", ["name=","count=","time","basic","source","hashtags","mentions","geo=","find=","stime=","etime=", "sdate=","edate=","pics=","output="])
		for o, a in opts:
			if o in ("-n", "--name"):
				arg_name = a
			elif o in ("-c", "--count"):
				arg_count = a
			elif o in ("-t", "--time"):
				arg_time = 1
			elif o in ("-b", "--basic"):
				arg_basic = 1
			elif o in ("-s", "--source"):
				arg_source = 1
			elif o in ("-h", "--hashtags"):
				arg_hashtags = 1
			elif o in ("-m", "--mentions"):
				arg_mentions = 1
			elif o in ("-g", "--geo"):
				arg_geofile = a
			elif o in ("-f", "--find"):
				arg_find = a
			elif o in ("--stime"):
				arg_stime = a
			elif o in ("--etime"):
				arg_etime = a
			elif o in ("--sdate"):
				arg_sdate = a
			elif o in ("--edate"):
				arg_edate = a
			elif o in ("-p", "--pics"):
				arg_pics = a
			elif o in ("-o", "--output"):
				arg_output = a

	except:
		show_usage()
		show_final_message()
		sys.exit(1)

################
# Show final message
################
def show_final_message():
	try:
		tdelta = datetime.datetime.now() - sdate
		hours, remainder = divmod(tdelta.seconds, 3600)
		minutes, seconds = divmod(remainder, 60)
		print_data("\tElapsed time: %02d:%02d:%02d" % (hours, minutes, seconds)	)
		print_data("")
		print_data("See you soon!")
		print_data("")
		sys.exit(0)

	except Exception, e:
		print "\n[ show_final_message() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Get basic info for twitter user name
################
def get_basic_info():
	try:
		print_data(chr(27) + color + "\tAccount info" + chr(27) + "[0m")
		print_data("\t-------------------")
		print_data("\tScreen Name:\t\t " + user.screen_name.encode('utf-8'))
		print_data("\tUser name:\t\t " + user.name.encode('utf-8'))
		print_data("\tTwitter Unique ID:\t " + str(user.id))
		print_data("\tAccount created at:\t " + user.created_at.strftime('%m/%d/%Y'))
		print_data("\tFollowers:\t\t " + str(user.followers_count))
		print_data("\tTweets:\t\t\t " + str(user.statuses_count))
		print_data("\tLocation:\t\t " + str(user.location.encode('utf-8')))
		print_data("\tDescription:\t\t " + str(user.description.encode('utf-8')))
		print_data("\tURL:\t\t\t " + str(user.url))
		print_data("\tProfile image URL:\t " + str(user.profile_image_url))
		print_data("")

	except Exception, e:
		print "\n[ basic_info() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Get source
################
def get_source(tweet_source, tweet_created_at):
	try:
		add = 1
		for index, item in enumerate(source):
			if tweet_source == item[0]:
				add = 0	
		if add:
			source.append([tweet_source, str(tweet_created_at.strftime('%m/%d/%Y')), str(tweet_created_at.time())])

	except Exception, e:
		print "\n[ get_source() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Get hashtags user mentions
################
def get_hashtags_user_mentions(request, name, tag, tweet_info, tweet_created_at):
	try:
		tmp = ""
		for i in tweet_info:
			if i[name].encode('utf-8'):
				tmp = tmp + tag + i[name].encode('utf-8') + " "
		if len(tmp):
			if not [tmp, tweet_created_at.strftime('%m/%d/%Y'), tweet_created_at.time()] in request:
				if arg_time:
					request.append([tmp, tweet_created_at.strftime('%m/%d/%Y'), tweet_created_at.time()])
				else:
					add = 1
					for m in request:
						if tmp.lower() in m[0].lower(): 
							add = 0
					if add:
						request.append([tmp, tweet_created_at.strftime('%m/%d/%Y'), tweet_created_at.time()])

	except Exception, e:
		print "\n[ get_hashtags_user_mentions() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Get geo info
################
def get_geo_info(tweet_place, tweet_geo, tweet_created_at):
	try:
		splace = ""
		sgeo = ""
		add = 0
		if tweet_place:
			splace = tweet_place.name.encode('utf-8')
			add = 1
		if tweet_geo:
			sgeo = tweet_geo['coordinates']
			add = 1
		if add:
			sinfo = splace + " " + str(sgeo)
		else:
			sinfo = ""		
		geo_info.append([sinfo, str(tweet_created_at.strftime('%m/%d/%Y')), str(tweet_created_at.time())])

	except Exception, e:
		print "\n[ get_geo_info() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Get tweets with word
################
def get_tweets_with_word(tweet_text, tweet_created_at):
	try:
		if arg_find.lower() in tweet_text.lower() or arg_output:
			tweet_with_word.append([tweet_text, str(tweet_created_at.strftime('%m/%d/%Y')), str(tweet_created_at.time())])

	except Exception, e:
		print "\n[ get_tweets_with_word() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Get user images
################
def get_user_images(tweet_text, tweet_created_at):
	try:
		urlimg = ""
		spic = tweet_text.find("http://t.co/")
		if spic > -1:
			if (spic+22) < 141:
				url = tweet_text[spic:spic+22]
				response = urllib2.urlopen(url)
				if response:
					html = response.read()
					if html:
						findurl = html.find("https://pbs.twimg.com/media/")
						if findurl > -1:
							urlimg = html[findurl:findurl+47]
							if arg_pics == "1":
								if not os.path.isdir(user.screen_name):
									os.mkdir(user.screen_name)
								img = urllib2.urlopen(urlimg).read()
								filename = urlimg.split('/')[-1]
								if not os.path.exists(user.screen_name+"/"+filename):
									f = open(user.screen_name+"/"+filename, 'wb')
									f.write(img)
									f.close()

		tweet_images.append([urlimg, str(tweet_created_at.strftime('%m/%d/%Y')), str(tweet_created_at.time())])

	except Exception, e:
		tweet_images.append(["", "", ""])
		#print "\n[ get_user_images() Error ]\n\tError message:\t ", e, "\n"
		return 1

################
# Is valid
################
def is_valid(tweet):
	try:
		valid = 1
		time = str(tweet.created_at.time())
		if time < arg_stime or time > arg_etime:
			valid = 0

		date = str(tweet.created_at.strftime('%Y/%m/%d'))
		if date < arg_sdate or date > arg_edate:
			valid = 0

		return valid

	except Exception, e:
		print "\n[ is_valid() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Get detail info for twitter user name
################
def get_details():
	try:
		page = 1
		tweets = 0		
		while True:
			timeline = api.user_timeline(screen_name=user.screen_name, include_rts=True, count=arg_count, page=page)
			if timeline:
				for tweet in timeline:
					tweets += 1
					if is_valid(tweet):
						if arg_source:
							get_source(tweet.source.encode('utf-8'), tweet.created_at)
						if arg_hashtags:
							get_hashtags_user_mentions(hashtags, 'text', '#', tweet.entities['hashtags'], tweet.created_at)
						if arg_mentions:				
							get_hashtags_user_mentions(user_mentions, 'screen_name', '@', tweet.entities['user_mentions'], tweet.created_at)
						if arg_pics == "1" or (arg_pics == "0" and arg_geofile):
							get_user_images(tweet.text.encode('utf-8'), tweet.created_at)
						if arg_geofile:				
							get_geo_info(tweet.place, tweet.geo, tweet.created_at)
						if arg_find or arg_geofile:
							get_tweets_with_word(tweet.text.encode('utf-8'), tweet.created_at)

					sys.stdout.write("\r\t" + str(tweets) + " tweets analyzed")
					sys.stdout.flush()										
					if tweets >= int(arg_count):
						print
						break
			else:
				break
			page += 1
			if tweets >= int(arg_count):
				break
		print 
	except Exception, e:
		print "\n[ get_details() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)


################
# Show tweet info
################
def show_tweet_info(tweet_info, header):
	try:
		if arg_time:
			print_data(chr(27) + color + "\tDate         Time       " + header + chr(27) + "[0m")
		else:
			print_data(chr(27) + color + "\tDate         " + header + chr(27) + "[0m")
		print_data("\t------------------------------------")

		c = 0
		for i in tweet_info:
			if len(i[0]) > 1:
				if arg_time:
					print_data("\t" + str(i[1]) + " - " + str(i[2]) + " - " + str(i[0]))
				else:
					print_data("\t" + str(i[1]) + " - " + str(i[0]))
				c = c + 1	

		print_data ("\n\t" + str(c) + " results.")		
		print_data ("")

	except Exception, e:
		print "\n[ show_tweet_info() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)


################
# Generates KML file
################
def generates_geofile(geo_info, tweets):
	kml_file_content = ""
	kml_file_header = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://earth.google.com/kml/2.2\">\n<Folder>\n"
	kml_file_body = ""
	kml_file_foot = "</Folder>\n</kml>"
	lat = ""
	lon = ""
	cdata = ""
	header = ""
	content = ""
	try:
		f = open(arg_geofile, "w")
		c = 0
		for i in geo_info:
			photo = ""
			scoordinates = str(i[0]).find("[")
			ecoordinates = str(i[0]).find("]")
			lat = str(i[0])[scoordinates+1:str(i[0]).find(",")]
			lon = str(i[0])[str(i[0]).find(",")+2:ecoordinates]
			if scoordinates > 0 and ecoordinates > 0:
				header = "<table bgcolor=\"#000000\" width=\"100%\"><tr><td><font color=\"white\"><b>" + program_name + " " + program_version + "</b></font><td align=\"right\"><font color=\"white\">@vaguileradiaz</font></td></tr></table>"
				content = "<table width=\"100%\"><tr><td width=\"48\"><img src=\""+user.profile_image_url+"\"></td><td bgcolor=\"#cde4f3\"><b>" + user.name.encode('utf-8') + "</b> @" + user.screen_name.encode('utf-8') + "<br>" + tweets[c][0] + "</td></tr></table>"
				if arg_pics:
					if tweet_images[c][0]:
						photo = " [Photo] "
						content += "<table width=\"100%\"><tr><td><img src=\"" + tweet_images[c][0] + "\"></td></tr></table>"
				cdata = "\t\t<![CDATA[" + header + content + "]]>\n"
				snippet = str(i[0][0:scoordinates-1].replace('&','and')) + photo
				kml_file_body += "\t<Placemark>\n"
				kml_file_body += "\t\t<name>" + str(i[1]) + " - " + str(i[2]) + "</name>\n"
				kml_file_body += "\t\t<Snippet>" + snippet + "</Snippet>\n"
				kml_file_body += "\t\t<description>\n" + cdata + "\t\t</description>\n"				
				kml_file_body += "\t\t<Point>\n"
				kml_file_body += "\t\t\t<coordinates>" + lon + "," + lat + "</coordinates>\n"
				kml_file_body += "\t\t</Point>\n"
				kml_file_body += "\t</Placemark>\n"
			c = c + 1
		kml_file_content = kml_file_header + kml_file_body + kml_file_foot
		f.write(kml_file_content)
		f.close()			

	except Exception, e:
		print "\n[ generates_geofile() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

################
# Main function
################
def main():
	global user
	global fd

	try:
		show_credits()
		get_options()
		if arg_output:
			fd = open(arg_output, "w")
		if arg_name == "" :
			show_usage()
		else:
			if arg_basic or arg_source or arg_hashtags or arg_mentions or arg_find or arg_geofile or arg_pics == "1" or (arg_pics == "0" and arg_geofile):
				user = api.get_user(arg_name)
				print_data ("Looking info for @"  + user.screen_name)
				print_data ("")				
				if arg_basic:
					get_basic_info()
				if arg_source or arg_hashtags or arg_mentions or arg_find or arg_geofile or arg_pics:
					get_details()
				if arg_source:
					show_tweet_info(source, "Source")
				if arg_hashtags:
					show_tweet_info(hashtags, "Hashtags")
				if arg_mentions:
					show_tweet_info(user_mentions, "User mentions")
				if arg_find:
					show_tweet_info(tweet_with_word, "Word [" + arg_find + "]")
				if arg_geofile:
					show_tweet_info(geo_info, "Geolocation information")
					generates_geofile(geo_info, tweet_with_word)							
			else:
				show_usage()

		show_final_message()
		if arg_output:
			fd.close()			
	except Exception, e:
		print "\n[ main() Error ]\n\tError message:\t ", e, "\n"
		sys.exit(1)

main()

