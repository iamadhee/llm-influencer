from langchain_core.language_models import BaseChatModel


class BaseWorker:
    agent_state: dict
    llm: BaseChatModel
