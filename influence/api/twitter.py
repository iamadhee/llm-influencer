import tweepy

def tweet(filename, text, config):
    auth = tweepy.OAuth1UserHandler(
        consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        access_token=config['access_token'],
        access_token_secret=config['access_token_secret']
    )

    api = tweepy.API(auth)

    client = tweepy.Client(
        bearer_token=config['bearer_token'],
        consumer_key=config['consumer_key'],
        consumer_secret=config['consumer_secret'],
        access_token=config['access_token'],
        access_token_secret=config['access_token_secret']  
    )

    media = api.media_upload(filename=filename)
    print("MEDIA: ", media)

    tweet = client.create_tweet(text=text, media_ids=[media.media_id_string])
    print("TWEET: ", tweet)

