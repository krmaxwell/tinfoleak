by Vicente Aguilera Diaz (@vaguileradiaz)

tinfoleak
=========

Get detailed information about the activity of a Twitter user.

tinfoleak is a simple Python script that allows users to obtain:

- basic information about a Twitter user (name, picture, location, followers, etc.)
- devices and operating systems used by the Twitter user
- applications and social networks used by the Twitter user
- place and geolocation coordinates to generate a tracking map of locations visited
- show user tweets in Google Earth!
- hashtags used by the Twitter user and when are used (date and time)
- user mentions by the the Twitter user and when they occurred (date and time)
- topics used by the Twitter user

You can filter all the information by:

- start date / time
- end date / time
- keywords

Requirements
------------
You need to have installed [Tweepy](https://github.com/tweepy/tweepy) (Twitter API library for Python) in your system.

Execution
---------

The first time you run this script, you need to assign the OAuth settings.

1. Edit "tinfoleak.py" with your favorite editor ;-)
2. Assign values to these variables (see [instructions](https://dev.twitter.com/discussions/631)):

    - CONSUMER_KEY
    - CONSUMER_SECRET
    - ACCESS_TOKEN
    - ACCESS_TOKEN_SECRET

3. Save "tinfoleak.py"
4. Execute "tinfoleak.py"
