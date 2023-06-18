from langchain.chat_models import ChatOpenAI
import time

class GPT3:
    API_RATE_LIMIT = 3  # Maximum number of API calls per minute
    call_times = []  # Track the timestamps of all API calls

    def __init__(self, temperature=0.9):
        self.llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=temperature)

    def run(self, prompt):
        current_time = time.time()

        # Remove the timestamps older than 1 minute
        GPT3.call_times = [t for t in GPT3.call_times if t >= current_time - 60]

        if len(GPT3.call_times) >= self.API_RATE_LIMIT:
            # If rate limit exceeded, calculate the time to wait
            time_to_wait = 60 - (current_time - GPT3.call_times[0]) + 1
            time.sleep(time_to_wait)  # Wait until the rate limit is reset

        response = self.llm.predict(prompt)
        GPT3.call_times.append(time.time())  # Store the timestamp of the API call

        if len(GPT3.call_times) > 9:
            GPT3.call_times = GPT3.call_times[-9:]

        return response