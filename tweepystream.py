import sys
import tweepy

from pymongo import Connection
from pymongo.code import Code

#'''
#Open a connection to MongoDb (localhost)
connection =  Connection()
db = connection.tweets

#Remove any existing data
db.tweets.remove()

# Query terms
loc = -38, 16, -22, 37  #-122.75,36.8,-121.75,37.8,-74,40,-73,41
Q = sys.argv[1:] 

# Get these values from your application settings
CONSUMER_KEY = 'W8ovxlTgVyMG9BsZ055F5A'
CONSUMER_SECRET = '43Bb4v3fKtS2wguvIVs1dh3bMGaMs0pQeQQsAitHRzs'

# Get these values from the "My Access Token" link located in the
# margin of your application details, or perform the full OAuth
# dance

ACCESS_TOKEN = '15775653-dKG6p7gRAHxjhuMlL6c2gF4djvpLFbuGqEP1ME1AU'
ACCESS_TOKEN_SECRET = 'n68hs66aWZuAMyjCwVgTlZy6hwGkiPGVNRsNkx08E'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


# Note: Had you wanted to perform the full OAuth dance instead of using
# an access key and access secret, you could have uses the following 
# four lines of code instead of the previous line that manually set the
# access token via auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
# 
#auth_url = auth.get_authorization_url(signin_with_twitter=True)
# webbrowser.open(auth_url)
# verifier = raw_input('PIN: ').strip()
# auth.get_access_token(verifier)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            db.tweets.insert({'text': status.text})
            print status.text
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print status_code
        #print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

# Create a streaming API and set a timeout value of 60 seconds
# Use OAuth to authenticate.
streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)
# Optionally filter the statuses you want to track by providing a list
# of users to "follow"

print 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),)

streaming_api.filter(follow=None, locations=loc, track=Q)