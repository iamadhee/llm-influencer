import os
import warnings
from datetime import datetime

from modules.quoter import Quoter
from modules.tweet_storm import TweetStorm

warnings.filterwarnings('ignore')
import configparser
import logging
from pathlib import Path

today = datetime.now().strftime('%d%b%y')

current_directory = Path().cwd()
influence_directory = current_directory / 'influence'

logging.getLogger('influencer')
log_name = influence_directory / f"logs/{today}.log"
log_name.touch()
logging.basicConfig(filename=log_name,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

config_parser = configparser.RawConfigParser()
config_parser.read(influence_directory / 'config.ini')

os.environ["OPENAI_API_KEY"] = config_parser['openai']['api_key']


class Orchestrator:
    def __init__(self):
        self.quoter = Quoter(config=config_parser)
        self.tweet_storm = TweetStorm(config=config_parser)

    def tweet(self):
        self.quoter.run()
        self.tweet_storm.run()


if __name__ == '__main__':
    orchestrator = Orchestrator()
    orchestrator.tweet()
