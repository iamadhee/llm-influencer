<div align="center">
<img width="200px" src="https://raw.githubusercontent.com/iamadhee/llm-influencer/main/assets/influencer.png">
<h1>LLM Influencer</h1></div>

<div align="center">
Your AI-powered content generator
</div>


## About
This project is an experimentation with AI, that aims on AI-Driven content generation. The aim is to be able to generate various types of content, such as podcasts, articles, and more using AI.

## Installation

1. Clone the repository
2. Install the required dependencies using `poetry install`
   - This project uses `poetry` for dependency management, so make sure you have it installed. If not, you can install it using `pip install poetry`

## Usage
1. Create a `.env` file in the root directory of the project, there is an example `.env.example` file provided. Fill in the required environment variables.
2. If you want, you can play around with the `config.toml` file to change the configurations of the content. Each type of content has its own section in the config file.
3. To create content of your choice, run the following command:
    ```bash
    python generate.py <type> <description>
    ```
    - `<type>` is the type of content you want to generate. Currently, the following types are supported:
        - `podcast` - For now this is the only type of content supported.
    - `<description>` is the description of the content you want to generate.

---

## Contributing
Currently, only podcast generation is supported with LLM-Influencer. We are working on adding more content types. If you'd like to contribute to this project, please feel free to submit a pull request.

## License
This project is licensed under the Apache 2.0 License.






