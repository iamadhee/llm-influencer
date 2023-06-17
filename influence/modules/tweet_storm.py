from langchain.chat_models import ChatOpenAI
from prompts.storm import STORM_PROMPT, NOTE_TEXT, THREAD_STARTER
from twitter_text import parse_tweet
import logging
from pathlib import Path
from api.twitter import Twitter
import yaml
import random
from ast import literal_eval
import re

logging.getLogger('influencer')

current_directory = Path().cwd()
influence_directory = current_directory / 'influence'
config_path = influence_directory / 'configs/storm.yaml'

with open(config_path, 'rb') as f:
    twitter_config = yaml.safe_load(f)

aspect = random.choice(list(twitter_config.keys()))
theme = f"{aspect} ({random.choice(twitter_config[aspect])})"
logging.info(f"THEME: {theme}")


class TweetStorm:
    def __init__(self, config) -> None:
        self.twitter_config = config['twitter']
        self.twitter_api = Twitter(config=self.twitter_config)
        self.chat_model = ChatOpenAI(temperature=0.9, model='gpt-3.5-turbo')

    def generate_storm(self):
        prompt = STORM_PROMPT.format(theme=theme)
        logging.info(f"PROMPT: {prompt}")
        result = self.chat_model.predict(prompt)
        tweet_dict = self.parse_result(result)
        return tweet_dict

    def parse_result(self, result):
        tweet_dict = literal_eval(result)
        return tweet_dict

    def run(self):
        tweet_dict = self.generate_storm()
        logging.info(f"RESULT: {tweet_dict}")
        rephrased_topic = tweet_dict['rephrased_topic']
        tweets = [tweet_dict[k] for k in tweet_dict.keys() if k != 'rephrased_topic']
        primary_tweet = THREAD_STARTER.format(rephrased=rephrased_topic)

        tweet_id = self.twitter_api.tweet(text=primary_tweet)

        for index, tweet in enumerate(tweets, 1):
            tweet = re.sub('#(\w+)', '', tweet)
            index = f'{index}/{len(tweets)}: '
            tweet_text = index + tweet
            tweet_id = self.twitter_api.reply_to_tweet(tweet_id=tweet_id, text=tweet_text)

        self.twitter_api.reply_to_tweet(tweet_id=tweet_id, text=NOTE_TEXT)
