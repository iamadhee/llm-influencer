import warnings
from datetime import datetime
from modules.quoter import Quoter
import os

warnings.filterwarnings('ignore')
import configparser
import logging
from pathlib import Path

today = datetime.now().strftime('%d%b%y')

logger = logging.getLogger('influencer')

cur_path = Path().cwd() / 'influence'

config = configparser.RawConfigParser()
config.read(cur_path / 'config.ini')

logname = cur_path / f"logs/{today}.log"
logname.touch()
logging.basicConfig(filename=logname,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

config = configparser.RawConfigParser()
config.read(cur_path / 'config.ini')

os.environ["OPENAI_API_KEY"] = config['openai']['api_key']

class Orchestrator:

    def __init__(self):
        self.quoter = Quoter(config=config)
        pass

    def tweet(self):
        self.quoter.run()

if __name__=='__main__':
    orchestrator = Orchestrator()
    orchestrator.tweet()