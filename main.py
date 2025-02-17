# This is a function that will implement the ReAct agent
from dotenv import load_dotenv
from langchain.agents import tool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.tools.render import render_text_description
from langchain.agents.format_scratchpad import (
    format_log_to_str,
)  # Utility function to format the agent's thoughts, actions, and observations
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools import Tool
from typing import Union, List
from langchain.schema import AgentAction, AgentFinish
from callbacks import AgentCallbackHandler

load_dotenv()


# The @tool decorator is a LangChain utility function that creates a custom tool
# More info: https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/
@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip('"')  # stripping away non aplhabetical characters

    return len(text)


def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


if __name__ == "__main__":
    print("hello world")
    tools = [get_text_length]

    # chain of thought prompt template because we're asking the model to think step by step.
    # it's also a few shots prompt template because we're providing a few examples of how we want the model to behave.
    # This is an implementation of the ReAct agent, reasoning and action.
    # More info: https://python.langchain.com/v0.1/docs/modules/agents/agent_types/react/
    # agent_scratchpad is a variable that will be used to store the agent's thoughts, actions, and observations
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    # we need the stop to let the LLM know when to stop to wait for the tool call results, otherwise it will keep generating values which would be incorrect halucinations
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        stop="\nObservation",
        callbacks=[AgentCallbackHandler()],
    )
    intermediate_steps = []

    agent = (
        {
            "input": lambda x: x["input"],
            # Using the format_log_to_str function to format the agent's thoughts, actions, and observations
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()  # This is a parser that will parse the agent's output into a structured format
    )

    agent_step = ""

    while not isinstance(agent_step, AgentFinish):
        agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
            {
                "input": "What is the length of the word 'DOG' in characters?",
                "agent_scratchpad": intermediate_steps,
            }
        )

        print(agent_step)

        if isinstance(agent_step, AgentAction):
            tool_name = agent_step.tool
            tool_to_use = find_tool_by_name(tools, tool_name)
            tool_input = agent_step.tool_input

            # Here we're invoking the tool with the tool input
            observation = tool_to_use.func(str(tool_input))
            print(f"{observation=}")

            # this is the history of the agent's thoughts, actions, and observations
            intermediate_steps.append((agent_step, str(observation)))

    print(f"Steps: {format_log_to_str(intermediate_steps)}")

    if isinstance(agent_step, AgentFinish):
        print("### AgentFinish ###")
        print(agent_step.return_values)
