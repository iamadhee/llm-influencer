GENERATE_SEARCH_QUERIES_PROMPT = """
                    Generate {max_iterations} precise Google search queries aimed at conducting thorough, 
                    objective research on the given topic and only about the given topic. You should not deviate from 
                    the given topic. All the queries you generate should only be for the given topic. Think step-by-step very carefully and draft the search queries. These queries 
                    should cover all key aspects of the topic, providing a comprehensive understanding of its various 
                    dimensions. The goal is to develop a well-rounded, evidence-based opinion by gathering relevant 
                    data from multiple perspectives. Assume the current date is {current_time} if required.\n\n\n
                    For the very last time, let me be very clear. I want search queries that can directly be executed in google and not instructions.
                    DO NOT GIVE ANY INSTRUCTIONS.

                    The given topic is "{task}".
                    """

SUMMARIZE_PROMPT = (
    "Write a detailed and comprehensive summary of the following search results, ensuring that no key information is overlooked:\n"
    f"{'=' * 30}\n"
    "{search_content}\n"
    f"{'=' * 30}\n"
    "The summary must focus exclusively on the given topic, which is of utmost importance. It should not deviate from this topic and should thoroughly cover all key aspects. As this summary will be included in an extensive report, clarity, precision, and direct relevance to the topic are essential. "
    "Accuracy and depth are crucial, as this report significantly impacts my career. If needed, please note the current date: {current_time}. "
    "I do not want instructions, I want executable google search queries. Return the search queries as a list and return only the list.\n\n"
    "**Topic:**\n"
    f"{'-' * 15}\n"
    "{task}\n"
    f"{'-' * 15}\n"
)

COMBINE_RESEARCH_DATA_PROMPT = (
    "Integrate the following research summaries into a cohesive and detailed report:\n"
    f"{'='*30}\n"
    "{combined_summary}\n"
    f"{'='*30}\n\n"
    "Ensure that the report is professionally crafted, meticulously organized, and concise, "
    "clearly articulating all key points, insights, and nuances from the research. Attention to "
    "detail is paramount, as this report will be provided to a professional writer who will further "
    "refine the content. Focus on clarity, coherence, and logical flow, making it easy for the "
    "reader to grasp the connections and significance of the summarized information.\n"
    "The sole focus of this report should be on the original topic, which you'll be provided with. "
    "The current date ({current_time}) if relevant, to ensure the report is timely and contextually appropriate.\n\n"
    "Research Summaries --> \n"
    "{combined_summary}"
    "Original Topic --> \n"
    'the topic is "{task}"'
)
