from models.gpt3 import GPT3
from prompts.storm import STORM_PROMPT, NOTE_TEXT, THREAD_STARTER
from twitter_text import parse_tweet
from pathlib import Path
from api.twitter import Twitter
import yaml
import random
from ast import literal_eval
import re
from modules.base import BaseModule
from utils import setup_custom_logger

logger = setup_custom_logger()

current_directory = Path().cwd()
influence_directory = current_directory / 'influence'
config_path = influence_directory / 'configs/storm.yaml'

with open(config_path, 'rb') as f:
    aspects_config = yaml.safe_load(f)

class TweetStorm(BaseModule):
    def __init__(self, config) -> None:
        self.twitter_config = config['twitter']
        self.twitter_api = Twitter(config=self.twitter_config)
        self.chat_model = GPT3()

    def select_theme(self):
        aspect = random.choice(list(aspects_config.keys()))
        theme = f"{aspect} ({random.choice(aspects_config[aspect])})"
        logger.info(f"THEME: {theme}")
        return theme

    def generate_storm(self):
        theme = self.select_theme()
        prompt = STORM_PROMPT.format(theme=theme)
        logger.info(f"PROMPT: {prompt}")
        result = self.chat_model.run(prompt)
        tweet_dict = self.parse_result(result)
        return tweet_dict

    def parse_result(self, result):
        tweet_dict = literal_eval(result)
        return tweet_dict

    def run(self):
        tweet_dict = self.generate_storm()
        logger.info(f"RESULT: {tweet_dict}")
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
