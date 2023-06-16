import random
from api.twitter import Twitter
import pandas as pd
import requests
import utils
from datetime import datetime

from langchain.chat_models import ChatOpenAI
from openai import Image
from prompts.image import IMAGE_PROMPT
from prompts.quote import NOTE_TEXT, QUOTE_PROMPT
from twitter_text import parse_tweet
import time
import re
import logging
from pathlib import Path

logging.getLogger('influencer')

cur_path = Path().cwd() / 'influence'
data_path =  Path().cwd() / 'data/finalq.json'
today = datetime.now().strftime('%d%b%y')

class Quoter:

    SSL_VERIFY = False

    def __init__(self, config):
        self.config = config['twitter']
        self.tweeter = Twitter(config=self.config)
        self.llm = ChatOpenAI(temperature=.9, model = 'gpt-3.5-turbo')
        quotes_df = pd.read_json(open(data_path,'r'))

        auth_list = quotes_df['Author'].unique().tolist()
        self.auth = auth_list[random.randint(0,len(auth_list))]
        auth_quotes = quotes_df[quotes_df['Author'] == self.auth]['Quote'].tolist()
        q_list = random.sample(auth_quotes, 4)
        self.fquotes = utils.format_quotes(q_list=q_list)

    def create_quote(self):
        q_prompt = QUOTE_PROMPT.format(author=self.auth.title(), quotes=self.fquotes)
        self.quote = self.llm.predict(q_prompt)
        self.quote = re.sub('#(\w+)|"','',self.quote)
        logging.info(f'{q_prompt}\n----------')
    
    def inspire_image(self):
        i_prompt = IMAGE_PROMPT.format(quote=self.quote)
        dalle_prompt = self.llm.predict(i_prompt)

        logging.info(f'{i_prompt}\n----------')
        logging.info(f'{dalle_prompt}\n----------')
        return dalle_prompt

    def create_image(self, prompt):
        image_url = Image.create(prompt=prompt, size='1024x1024')['data'][0]['url']
        filepath = cur_path / f"gen_images/{today}.jpg"
        filepath.touch()
        response = requests.get(url=image_url, stream=True, verify=self.SSL_VERIFY)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    
    def run(self):
        try:
            valid_tweet=False
            while not valid_tweet:
                self.create_quote()
                if parse_tweet(self.quote).weightedLength <= 145:
                    prompt = self.inspire_image()
                    filepath = self.create_image(prompt)
                    valid_tweet=True
                else:
                    logging.warn(f'QUOTE:  {self.quote} ')
                    logging.warn('tweet not within limit - retrying quote generation')
                    time.sleep(30)

            tweet_text = self.quote
            logging.info(f'\n\nTWEET TEXT:\n{tweet_text}\n{NOTE_TEXT}')
            tweet_id = self.tweeter.tweet(filename=filepath, text=tweet_text)
            self.tweeter.reply_to_tweet(tweet_id=tweet_id, text=NOTE_TEXT)

        except Exception as e:
            logging.error(e)

