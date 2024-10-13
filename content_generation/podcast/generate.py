import ast
import asyncio
import time
from pathlib import Path

from content_generation.base import BaseContentGenerator
from content_generation.podcast import config
from influencer.agents.worker.researcher.agent import Researcher
from influencer.agents.worker.podcast_writer.agent import PodcastWriter
from influencer.text_to_speech import ScriptToSpeech
from langchain_community.callbacks import get_openai_callback

from utils.loggerconfig import logger
from utils.utils import sanitize_script


class Podcast(BaseContentGenerator):
    def __init__(self):
        self.writer = PodcastWriter(
            host_name=config["host_name"],
            expert_name=config["expert_name"],
            show_name=config["show_name"],
        )
        self.researcher = Researcher(max_iterations=3)
        self.audio_generator = ScriptToSpeech(
            tts_model=config["tts_model"],
            host_voice=config["host_voice"],
            expert_voice=config["expert_voice"],
            intro_path=Path(__file__).parent / "music/intro.wav",
            outro_path=Path(__file__).parent / "music/outro.wav",
        )

    async def generate(self, **kwargs):
        start_time = time.time()
        with get_openai_callback() as cb:
            research_summary = await self.researcher.run(topic=kwargs["description"])
            script = await self.writer.run(content=research_summary)
            if isinstance(script, str):
                script = sanitize_script(script)
                script = ast.literal_eval(script)
            await self.audio_generator.run(dialogues=script)
            logger.info(f"Podcast generation costed: {cb.total_cost:.2f}$ 💰")
            end_time = time.time()
            logger.info(
                f"Time taken to generate podcast: {end_time - start_time:.2f} seconds 🕒"
            )

    def run(self, *args, **kwargs):
        asyncio.run(self.generate(**kwargs))
