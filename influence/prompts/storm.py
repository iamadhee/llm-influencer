STORM_PROMPT = '''I want you to act as a Twitter influencer similar to Naval Ravikant. Your task is to create a tweet storm consisting of 5 tweets per day on the provided theme. Add the rephrased theme name in rephrased_topic. Please provide the content in the following format, ensuring that each tweet is within the 140-character limit. Return the dictionary alone.

THEME: {theme}

```
{{
'rephrased_topic': '',
'tweet1': '',
'tweet2': '',
'tweet3': '',
'tweet4': '',
'tweet5': '',
'hashtags': ''
}}
```'''

NOTE_TEXT = '''Note: This tweet storm is entirely generated by an AI. This is in no way reflects my opinion or view on any subject. This is purely an experimentation with AI. You can find more details here: https://github.com/iamadhee/llm-influencer#readme'''

THREAD_STARTER = '''An AI's view on "{rephrased}" (a thread 🧵):'''


