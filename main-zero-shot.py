# This is a function that will implement the ReAct agent
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType, tool, AgentExecutor
from langchain_openai import ChatOpenAI

load_dotenv()


# The @tool decorator is a LangChain utility function that creates a custom tool
# More info: https://python.langchain.com/v0.1/docs/modules/tools/custom_tools/
@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip('"')  # stripping away non aplhabetical characters

    return len(text)

if __name__ == "__main__":
    llm = ChatOpenAI()
    agent_executor: AgentExecutor = initialize_agent(
        tools=[get_text_length],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    agent_executor.invoke({"input": "What is the length of the word 'DOG' in characters?"})

