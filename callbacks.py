from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from typing import Any, Dict, List


class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running"""
        print(f"### LLM Start ###")
        print(prompts[0])
        print("***************")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running"""
        print("### LLM Response ###")
        print(response.generations[0][0].text)
        print("***************")
