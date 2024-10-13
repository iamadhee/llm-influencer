from datetime import datetime
from datetime import timezone
from functools import cached_property

from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langgraph.graph import StateGraph, END, START
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

from influencer.agents.state import PodcastWriterState
from influencer.agents.worker import BaseWorker
from influencer.agents.worker.podcast_writer import GENERATE_SCRIPT_PROMPT
from utils.loggerconfig import logger


class Script(BaseModel):
    dialogues: list[str]


class PodcastWriter(BaseWorker):
    agent_state = PodcastWriterState
    llm = ChatOpenAI

    def __init__(
        self,
        host_name="Sarah Simmons",
        expert_name="David Orion",
        show_name="The Synth and Sentience Show",
    ):
        self.host_name = host_name
        self.expert_name = expert_name
        self.show_name = show_name

    @cached_property
    def graph(self):
        _workflow = StateGraph(self.agent_state)
        _workflow.add_node("generate_script", self.generate_script)
        _workflow.add_edge(START, "generate_script")
        _workflow.set_entry_point(key="generate_script")
        _workflow.add_edge("generate_script", END)
        return _workflow.compile()

    async def generate_script(self, state: PodcastWriterState):
        prompt = ChatPromptTemplate.from_messages(
            [
                HumanMessage(
                    GENERATE_SCRIPT_PROMPT.format(
                        host_name=self.host_name,
                        expert_name=self.expert_name,
                        show_name=self.show_name,
                        current_time=datetime.now(timezone.utc).strftime("%B %d, %Y"),
                        content=state["content"],
                    )
                )
            ]
        )
        script_llm = prompt | self.llm(model="o1-preview", temperature=1)
        script = await script_llm.ainvoke({"content": state["content"]})
        state["script"] = script.content
        return state

    async def run(self, content: str):
        logger.info("Writing the script for your podcast... 🎙️")
        script = await self.graph.ainvoke({"content": content})
        logger.info("Cooking up something delicious... 🍲")
        return script["script"]
