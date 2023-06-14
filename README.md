<div align="center">
<img width="200px" src="https://raw.githubusercontent.com/iamadhee/llm-influencer/main/assets/yellow_robot.png">
<h1>LLM Influencer 🦾</h1></div>

<div align="center">
Your daily dose of motivation from an AI
</div>

## What is llm-influencer ❓

LLM Influencer is an AI-powered Twitter influencer that generates and posts daily quotes along with captivating images. It utilizes the powerful combination of ChatGPT and DALL-E 2, two state-of-the-art models developed by OpenAI. This repository contains the code for running and maintaining the bot.

----

## How llm-influencer works ⚙️

LLM Influencer harnesses the creative power of GPT-3, a cutting-edge generative AI model, to generate all the quotes posted on Twitter. These quotes draw inspiration from the curated corpus stored in the [finalq.json](https://github.com/iamadhee/llm-influencer/blob/main/data/finalq.json) file. To enhance the visual appeal of the posts, LLM Influencer pairs each quote with stunning images crafted by the DALL-E 2 image generation model. 

<details>
  <summary><h2>Installation and Setup 🔨 </h2></summary>
  
  ### Installation
  clone this repository and install dependencies using `pip install -r requirements.txt`
  
  
  ### Setup
  create a file named `config.ini` within the `influence/` directory and copy the below fields and fill in with your own credentials. No need to use quotes.
  ```ini
  [twitter]
  bearer_token=
  consumer_key=
  consumer_secret=
  access_token=
  access_token_secret=

  [openai]
  api_key=
  ```
  
  If you have trouble finding you credentials head to the below links for help:
- [twitter-api](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret)
- [openai-api](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/)
  
  Once you've setup the config, you're good to go. To run the bot you just have to run `python3 influence`. This will create a quote, an image and posts it to the twitter account that you've provided. I've set this up as a cron job and you could too.

</details>

---

## Contributing 🤝

We welcome any type of contributions to this project. If you find a bug or have a feature request, please submit an issue on GitHub. If you would like to contribute code to the project, please submit a pull request. Your suggestions are always welcome !

----

## License :

llm-influencer is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/iamadhee_)
Head to [@iamadhee_](https://twitter.com/iamadhee_) to see the posts

