import os
import warnings
from modules.quoter import Quoter
from modules.tweet_storm import TweetStorm
import configparser
from pathlib import Path
from utils import setup_email_alerter
import yaml
import schedule
import time
from datetime import datetime
warnings.filterwarnings('ignore')

current_directory = Path().cwd()
influence_directory = current_directory / 'influence'

config_ini = configparser.RawConfigParser()
config_ini.read(influence_directory / 'config.ini')

with open(influence_directory / 'config.yaml', 'rb') as f:
    config_yml = yaml.safe_load(f) 

email_ini = config_ini['smtp']
logger = setup_email_alerter(alert_email=email_ini['alert_email'], app_pwd=email_ini['app_pwd'])

os.environ["OPENAI_API_KEY"] = config_ini['openai']['api_key']

class Orchestrator:
    def __init__(self):
        self.quoter = Quoter(config=config_ini)
        self.tweet_storm = TweetStorm(config=config_ini)
    
    def pick_item_by_date(self):
        job_list = config_yml['MODULES']
        total_items = len(job_list)
        current_date = datetime.now().day
        index = current_date % total_items
        if index == 0:
            index = total_items
        return job_list[index - 1].lower()

    def execute(self):
        module_name = self.pick_item_by_date()
        module = getattr(self, module_name)
        module.run()

if __name__ == '__main__':
    try:
        orchestrator = Orchestrator()
        schedule.every().day.at(config_yml['SCHEDULE_TIME']).do(orchestrator.execute)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        logger.error(e, exc_info=True)