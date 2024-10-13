import asyncio
from pathlib import Path
import random

from openai import AsyncOpenAI
from pydub import AudioSegment

from utils.loggerconfig import logger

async_client = AsyncOpenAI()

# nova - Female
# alloy - Male

AUDIO_FILE_PATH = Path(__file__).parent
PROJECT_PATH = Path(__file__).parents[2]

if not (PROJECT_PATH / "output/").exists():
    (PROJECT_PATH / "output/").mkdir(parents=True)

FINAL_OUTPUT_PATH = PROJECT_PATH / "output" / "podcast.wav"


class ScriptToSpeech:
    def __init__(
        self,
        intro_path,
        outro_path,
        host_voice="nova",
        expert_voice="alloy",
        tts_model="tts-1",
    ):
        self.dialogues = None
        self.host_voice = host_voice
        self.expert_voice = expert_voice
        self.tts_model = tts_model
        self.intro = AudioSegment.from_wav(intro_path)
        self.outro = AudioSegment.from_wav(outro_path)

    async def __script_to_speech(self, dialogue, voice, file_path):
        async with async_client.audio.speech.with_streaming_response.create(
            model=self.tts_model,
            voice=voice,
            input=dialogue,
            response_format="wav",
        ) as response:
            await response.stream_to_file(AUDIO_FILE_PATH / file_path)

    def __combine_audio(self):
        combined = AudioSegment.empty()

        # Fade-in with intro
        intro = self.intro.fade_out(5000)

        combined += intro  # Add intro at the beginning

        for d_count in range(len(self.dialogues)):
            audio_file_path = AUDIO_FILE_PATH / f"audio_{d_count}.wav"
            audio = AudioSegment.from_wav(audio_file_path)

            # Apply Dynamic Panning (Stereo Effect)
            if d_count % 2 == 0:  # Female speaker
                panning_fluctuation = random.uniform(-0.30, -0.10)
                pause_duration = random.uniform(0.50, 1.0) * 1000
            else:  # Male speaker
                panning_fluctuation = random.uniform(0.10, 0.30)
                pause_duration = random.uniform(0.70, 1.5) * 1000

            audio = audio.pan(panning_fluctuation)

            # Apply Volume Fluctuations (Simulate movement)
            audio = audio + random.uniform(
                -1.5, 1.5
            )  # Slight volume fluctuation (dB shift)

            # Pause between the speakers
            pause = AudioSegment.silent(duration=pause_duration)
            combined += audio + pause  # Append audio and pause

            audio_file_path.unlink(missing_ok=True)  # Delete the temporary audio file

        # Fade-out with outro
        outro = self.outro.fade_in(5000)
        combined += outro  # Add outro at the end

        # Export the combined podcast audio
        combined.export(FINAL_OUTPUT_PATH, format="wav")

    def __create_async_tasks(self):
        tasks = []
        for turn, dialogue in enumerate(self.dialogues):
            voice = self.expert_voice
            if turn % 2 == 0:
                voice = self.host_voice
            tasks.append(self.__script_to_speech(dialogue, voice, f"audio_{turn}.wav"))
        return tasks

    async def run(self, dialogues):
        self.dialogues = dialogues
        logger.info("Giving life to your script... 💫")
        tasks = self.__create_async_tasks()
        await asyncio.gather(*tasks)
        await asyncio.sleep(0)
        self.__combine_audio()
        logger.info("Your podcast is ready! 🎉")
        logger.info("Check out the generated podcast file at " + str(FINAL_OUTPUT_PATH))
