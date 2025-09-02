from email import message
import http
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio
async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                "args": ["math_server.py"],
                "transport": "stdio"
            },
            "weather": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable:http"
            }
        }
    )

    import os
    os.environ["GROQ_API_KEY"]="your_groq_api_key"

    tools=await client.get_all_tools()
    model=ChatGroq(model="qwen-qwq-32b")
    agent=create_react_agent(
        model,tools)


    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "What is 5 + 3?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)

    asyncio.run(main())