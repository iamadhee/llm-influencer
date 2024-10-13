import asyncio
from datetime import datetime
from datetime import timezone
from functools import cached_property

from influencer.agents.worker.researcher import COMBINE_RESEARCH_DATA_PROMPT
from influencer.agents.worker.researcher import (
    GENERATE_SEARCH_QUERIES_PROMPT,
    SUMMARIZE_PROMPT,
)

from influencer.agents.state import ResearcherState
from influencer.agents.worker import BaseWorker
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.tools import TavilySearchResults
from utils.loggerconfig import logger


class SplitSearchQueries(BaseModel):
    tasks: list[str]


class Researcher(BaseWorker):
    agent_state = ResearcherState
    llm = ChatOpenAI

    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations

    @cached_property
    def graph(self):
        _workflow = StateGraph(self.agent_state)
        _workflow.add_node("generate_search_queries", self.generate_search_queries)
        _workflow.set_entry_point(key="generate_search_queries")
        _workflow.add_node("do_research", self.do_research)
        _workflow.add_node("combine_research_data", self.combine_research_data)
        _workflow.add_edge("generate_search_queries", "do_research")
        _workflow.add_edge("do_research", "combine_research_data")
        _workflow.add_edge("combine_research_data", END)
        return _workflow.compile()

    def generate_search_queries(self, state: ResearcherState):
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    GENERATE_SEARCH_QUERIES_PROMPT.format(
                        max_iterations=self.max_iterations,
                        current_time=datetime.now(timezone.utc).strftime("%B %d, %Y"),
                        task=state["task"],
                    )
                ),
            ]
        )
        splitter_llm = prompt | self.llm(
            model="gpt-4o", temperature=0.3
        ).with_structured_output(SplitSearchQueries)
        split_queries = splitter_llm.invoke({"task": state["task"]})
        state["research_queries"] = split_queries.tasks
        logger.info("Building up search queries to execute... 🧱")
        return state

    def search_internet(self, query: str):
        search_tool = TavilySearchResults(
            max_results=2, include_raw_content=True, search_depth="advanced"
        )
        search_results = search_tool.invoke({"query": query})
        return search_results

    async def summarize(self, search_query, state: ResearcherState) -> str:
        search_results = self.search_internet(search_query)
        search_content = [
            _result["raw_content"] if "raw_content" in _result else _result["content"]
            for _result in search_results
        ]
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    SUMMARIZE_PROMPT.format(
                        search_content="\n\n----------\n\n".join(search_content),
                        current_time=datetime.now(timezone.utc).strftime("%B %d, %Y"),
                        task=state["task"],
                    )
                ),
            ]
        )
        summary_llm = prompt | self.llm(model="gpt-4o")
        summary_response = await summary_llm.ainvoke({"topic": state["task"]})
        return summary_response.content

    async def do_research(self, state: ResearcherState):
        research_queries = state["research_queries"]
        logger.info("Browsing the internet for information... 🔍")
        search_tasks = [self.summarize(query, state) for query in research_queries]
        logger.info("Summarizing the research results... ✒️")
        results = await asyncio.gather(*search_tasks)
        state["research_data"] = list(results)
        return state

    async def combine_research_data(self, state: ResearcherState):
        # Combine all the research summaries into a single summary
        combined_content = "\n\n".join(state["research_data"])
        prompt = ChatPromptTemplate.from_messages(
            [
                HumanMessage(
                    COMBINE_RESEARCH_DATA_PROMPT.format(
                        combined_summary=combined_content,
                        current_time=datetime.now(timezone.utc).strftime("%B %d, %Y"),
                        task=state["task"],
                    )
                )
            ]
        )
        logger.info("Collating all the research data... 📝")
        combined_llm = prompt | self.llm(model="o1-mini", temperature=1)
        final_summary = await combined_llm.ainvoke(
            {"combined_summary": combined_content}
        )
        state["final_report"] = final_summary.content
        return state

    async def run(self, topic: str):
        res = await self.graph.ainvoke({"task": topic})
        return res["final_report"]
