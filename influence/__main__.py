from langchain.chat_models import ChatOpenAI
import pandas as pd
import random
import utils
from prompts.quote import QUOTE_PROMPT
from prompts.image import IMAGE_PROMPT
from datetime import datetime
from openai import Image
import os
import requests
import warnings
from api.twitter import tweet
from pathlib import Path
warnings.filterwarnings('ignore')
import configparser
import logging

cur_path = Path().cwd() / 'influence'

config = configparser.RawConfigParser()
config.read(cur_path / 'config.ini')

os.environ["OPENAI_API_KEY"] = config['openai']['api_key']

class Prompter:

    def __init__(self):
        self.config = config
        self.llm = ChatOpenAI(temperature=.9, model = 'gpt-3.5-turbo')
        quotes_df = pd.read_json(open('data/finalq.json','r'))

        auth_list = quotes_df['Author'].unique().tolist()
        self.auth = auth_list[random.randint(0,len(auth_list))]
        auth_quotes = quotes_df[quotes_df['Author'] == self.auth]['Quote'].tolist()
        q_list = random.sample(auth_quotes, 4)
        self.fquotes = utils.format_quotes(q_list=q_list)

    def create_quote(self):
        q_prompt = QUOTE_PROMPT.format(author=self.auth.title(), quotes=self.fquotes)
        self.quote = self.llm.predict(q_prompt).replace('"','')
        i_prompt = IMAGE_PROMPT.format(quote=self.quote)
        dalle_prompt = self.llm.predict(i_prompt)

        logging.info(q_prompt,'\n','----------')
        logging.info(i_prompt,'\n','----------')
        logging.info(dalle_prompt,'\n','----------')

        return dalle_prompt

    def create_image(self, prompt):
        image_url = Image.create(prompt=prompt, size='1024x1024')['data'][0]['url']
        filepath = cur_path / f"gen_images/{datetime.now().strftime('%d%b%y')}.jpg"
        filepath.touch()
        response = requests.get(url=image_url, stream=True, verify=False)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    
    def run(self):
        prompt = self.create_quote()
        filepath = self.create_image(prompt)
        tweet(filename=filepath, text=self.quote, config=config['twitter'])


if __name__=='__main__':
    prompter = Prompter()
    prompter.run()




