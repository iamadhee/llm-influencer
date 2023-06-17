import tweepy
from twitter_text import parse_tweet

class Twitter:

    def __init__(self, config) -> None:
        auth = tweepy.OAuth1UserHandler(
        consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        access_token=config['access_token'],
        access_token_secret=config['access_token_secret']
        )

        self.api = tweepy.API(auth)

        self.client = tweepy.Client(
            bearer_token=config['bearer_token'],
            consumer_key=config['consumer_key'],
            consumer_secret=config['consumer_secret'],
            access_token=config['access_token'],
            access_token_secret=config['access_token_secret']  
        )

    def tweet(self, text, filename=None):
        client = self.client
        
        if filename:
            media = self.api.media_upload(filename=filename)
            tweet = client.create_tweet(text=text, media_ids=[media.media_id_string])
        else:
            tweet = client.create_tweet(text=text)
        return tweet[0]['id']

    def reply_to_tweet(self, tweet_id, text):
        reply = self.client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
        return reply[0]['id']
    
    def get_user_tweets(self, user):
        tweets = self.client.get_users_tweets(id=user,max_results=100)
        


