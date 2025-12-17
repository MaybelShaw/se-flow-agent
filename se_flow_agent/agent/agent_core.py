from langchain.agents import create_agent
from typing import Optional
from langchain_openai import ChatOpenAI, OpenAI
from se_flow_agent.settings import settings
from se_flow_agent.retriever.hybird_retriever import retrieve_tool

class AgentCore:
    def __init__(self):
        self.model = ChatOpenAI(
            model=settings.MODEL,
            base_url=settings.BASE_URL,
            api_key=settings.API_KEY,
        )

        self.agent = create_agent(
            model=self.model, tools=[retrieve_tool], system_prompt="你是一个乐于助人的助手。",
        )

    def invoke(self, prompt: str) -> str:
        return self.agent.invoke({"messages": [{"role": "user", "content": prompt}]})


if __name__ == "__main__":
    agent_core = AgentCore()
    response = agent_core.invoke("请帮我检索与人工智能相关的文档。")
    print(response)
