print("this is my twitter bot")
import tweepy 
import time
consumer_key = 'gYiM4AXsBCzTf4sIWv32O1Y2U' 
consumer_secret = 'QU295F6Ptvi22vVRCSt56uvaXSv3WLdnFzocnSDUMZfs0hY4lJ' 
access_token = '2977685302-GhcXlmTycUcvRL2TUqTsa2PUpD24d7fxihDOL2W' 
access_token_secret = 'ZXJhJpIxeesf1GjXReu1y5z7v7OrmYHAJ6gD6zeKPIrBp' 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

        
FILE_NAME = 'lastseen.txt'

def retrieve_lastseen(file_name):
    f_read = open(file_name, 'r')
    lastseen = int(f_read.read().strip())
    f_read.close()
    return lastseen

def store_lastseen(lastseen, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(lastseen))
    f_write.close()
    return

def reply_to_tweets():
    lastseen = retrieve_lastseen(FILE_NAME)
    mentions = api.mentions_timeline(
                        lastseen,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        lastseen = mention.id
        store_lastseen(lastseen, FILE_NAME)
        if '#hopzy' in mention.full_text.lower():
            print('Hopzy at your service')
            print('Please DM us your concern')
            api.update_status('@' + mention.user.screen_name +
                    'Please DM us your concern', mention.id)

while True:
    reply_to_tweets()
    time.sleep(15)
