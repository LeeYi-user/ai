import os
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq

# set up API key
os.environ["TAVILY_API_KEY"] = "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"

tools = [TavilySearchResults(max_results=1)]

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/react")

# Choose the LLM to use
llm = ChatGroq(api_key="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")

# Construct the ReAct agent
agent = create_react_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "奥利维亚·王尔德的男朋友是谁?他现在的年龄的0.23次方是多少? 用中文回答"})
