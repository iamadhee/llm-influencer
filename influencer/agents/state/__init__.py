from typing import List
from langgraph.graph import MessagesState


class ResearcherState(MessagesState):
    task: dict
    research_queries: List[str]
    research_data: List[str]
    final_report: str


class PodcastWriterState(MessagesState):
    content: str
    script: list[str]
