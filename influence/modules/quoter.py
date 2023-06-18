import random
from api.twitter import Twitter
import pandas as pd
import requests
import utils
from datetime import datetime
from models.gpt3 import GPT3
from openai import Image
from prompts.image import IMAGE_PROMPT
from prompts.quote import NOTE_TEXT, QUOTE_PROMPT
from twitter_text import parse_tweet
import re
from pathlib import Path
from utils import setup_custom_logger

logger = setup_custom_logger()

current_directory = Path().cwd()
influence_directory = current_directory / 'influence'
data_path = influence_directory / 'data/finalq.json'
current_date = datetime.now().strftime('%d%b%y')


class Quoter:
    SSL_VERIFY = False

    def __init__(self, config):
        self.twitter_config = config['twitter']
        self.twitter_api = Twitter(config=self.twitter_config)
        self.chat_model = GPT3()
        self.quotes_df = pd.read_json(open(data_path, 'r'))

    def create_quote(self):
        quote_prompt = QUOTE_PROMPT.format(author=self.selected_author.title(), quotes=self.formatted_quotes)
        self.quote = self.chat_model.run(quote_prompt)
        self.quote = re.sub('#(\w+)|"', '', self.quote)
        logger.info(f'{quote_prompt}\n----------')

    def inspire_image(self):
        image_prompt = IMAGE_PROMPT.format(quote=self.quote)
        dalle_prompt = self.chat_model.run(image_prompt)

        logger.info(f'{image_prompt}\n----------')
        logger.info(f'{dalle_prompt}\n----------')
        return dalle_prompt
    
    def select_quotes(self):
        quotes_df = self.quotes_df
        author_list = quotes_df['Author'].unique().tolist()
        self.selected_author = random.choice(author_list)
        author_quotes = quotes_df[quotes_df['Author'] == self.selected_author]['Quote'].tolist()
        selected_quotes = random.sample(author_quotes, 4)
        self.formatted_quotes = utils.format_quotes(q_list=selected_quotes)

    def create_image(self, prompt):
        image_url = Image.create(prompt=prompt, size='1024x1024')['data'][0]['url']
        file_path = influence_directory / f"gen_images/{current_date}.jpg"
        file_path.touch()
        response = requests.get(url=image_url, stream=True, verify=self.SSL_VERIFY)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return file_path

    def run(self):
        self.select_quotes()
        valid_tweet = False
        while not valid_tweet:
            self.create_quote()
            if parse_tweet(self.quote).weightedLength <= 145:
                prompt = self.inspire_image()
                file_path = self.create_image(prompt)
                valid_tweet = True
            else:
                logger.warn(f'QUOTE:  {self.quote} ')
                logger.warn('Tweet not within limit - retrying quote generation')

        tweet_text = self.quote
        logger.info(f'\n\nTWEET TEXT:\n{tweet_text}\n{NOTE_TEXT}')
        tweet_id = self.twitter_api.tweet(filename=file_path, text=tweet_text)
        self.twitter_api.reply_to_tweet(tweet_id=tweet_id, text=NOTE_TEXT)
