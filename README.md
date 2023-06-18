<div align="center">
<img width="200px" src="https://raw.githubusercontent.com/iamadhee/llm-influencer/main/assets/yellow_robot.png">
<h1>LLM Influencer 🦾</h1></div>

<div align="center">
Your daily dose of motivation from an AI
</div>

## What is llm-influencer ❓

LLM Influencer is a Twitter and social media bot that generates and posts daily content. It uses the power of ChatGPT and DALL-E 2 in the backend to generate diverse and inspiring content.

----

## Features 🚀

- Generates daily content for Twitter and other social media platforms.
- Easy plug-and-play modules for different types of content generation.
- Leveraging the capabilities of ChatGPT and DALL-E 2 for creative and unique outputs.
- Built-in scheduling for automatic posting at a desired time every day.
- Email notifications for job failure.

### Modules 🧩

The LLM Influencer offers a variety of modules that allow you to generate different types of content. These modules are designed to be easily customizable and enable you to tailor the content according to your preferences. Some examples of available modules are:

- **Quoter**: The Quoter module generates motivational quotes accompanied by captivating images. Drawing inspiration from renowned authors listed in the finalq.json file, this module creates insightful quotes that resonate with readers. Leveraging the power of DALL-E 2, the module generates visually appealing image that perfectly complements the quote and posts it along with the generated quote.

- **Tweet Storm**: The Tweet Storm module focuses on exploring various aspects of life. By selecting a major life aspect and a sub-aspect from the storm.yaml file, this module generates engaging content for a tweet storm. It crafts a series of connected tweets that delve into the chosen topic, offering valuable insights and perspectives.
  
---

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
  
  [smtp]
  alert_email=
  app_pwd=
  ```

`alert_email` is the email you want the mail to be sent to along with the error message when the job fails.
  
  If you have trouble finding your credentials head to the below links for help:
- [Twitter API keys generation](https://developer.twitter.com/en/docs/authentication/oauth-1-0a/api-key-and-secret)
- [OpenAI API key generation](https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/)
- [Gmail app password generation](https://support.google.com/mail/answer/185833?hl=en)

Once you're done setting up the `config.ini` file, head to the `config.yaml` file and tweak the configs if needed. The below is the list of configurables and their functionalities.

| configurable | description | allowed values |
| :---:   | :---: | :---: |
| SCHEDULE_TIME | The time at which you want to post to your social media handle |  `00:01` to `23:59` |
| MODULES | The modules you'd want shuffle between. Automatically chooses a module for a day if more than one is given. | `quoter`,`tweet_storm` |
  
Once you've setup the configs, you're good to go. To run the bot you just have to run `python3 influence`. That's it. You're done ! The Bot will automatically post content on a daily basis to your social media handle. You could run this inside a TMUX session to keep track of the job like me. If anything should break, you'll be notified through email.

</details>

---

## Contributing 🤝

We welcome any type of contributions to this project. If you find a bug or have a feature request, please submit an issue on GitHub. If you would like to contribute code to the project, please submit a pull request. Your suggestions are always welcome !

### Currently needed:

- **modules**: Video content generation module
- **social media**: Support for other social media handles like instagram, linkedin etc.,

----

## License 🗒️

llm-influencer is licensed under the Apache 2.0 License. See the `LICENSE` file for more information.

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
[![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/iamadhee_)
Visit [@iamadhee_](https://twitter.com/iamadhee_) to check out the posts