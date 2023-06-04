from langchain.chat_models import ChatOpenAI
import pandas as pd
import random
import utils
from prompts.quote import QUOTE_PROMPT
from prompts.image import IMAGE_PROMPT
from insta import post_image
from openai import Image
import os
import requests
import warnings
warnings.filterwarnings('ignore')

llm = ChatOpenAI(temperature=.9, model = 'gpt-3.5-turbo')

quotes_df = pd.read_json(open('data/finalq.json','r'))

auth_list = quotes_df.Author.unique().tolist()
auth = auth_list[random.randint(0,len(auth_list))]
auth_quotes = quotes_df[quotes_df.Author == auth]['Quote'].tolist()

q_list = random.sample(auth_quotes, 4)
fquotes = utils.format_quotes(q_list=q_list)

q_prompt = QUOTE_PROMPT.format(author=auth.title(), quotes=fquotes)
quote = llm.predict(q_prompt).replace('"','')

i_prompt = IMAGE_PROMPT.format(quote=quote)
dalle_prompt = llm.predict(i_prompt)

print(q_prompt,'\n','----------')
print(i_prompt,'\n','----------')
print(dalle_prompt,'\n','----------')

image_url = Image.create(prompt=dalle_prompt, size='1024x1024')['data'][0]['url']

filename = "my_image.jpg"
response = requests.get(url=image_url, stream=True, verify=False)
with open(filename, 'wb') as f:
    f.write(response.content)


    
















