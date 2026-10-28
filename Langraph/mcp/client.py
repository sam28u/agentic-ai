import asyncio
from dotenv import load_dotenv
from langchain.mcp import MCPAdapter
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

async def main():
    config = {
        "mcpServers": {
            "math": {
                "command": "python",
                "args": ["mathserver.py"],
                "transport": "stdio",
            },
            "weather": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable-http",
            },
        }
    }

    async with MCPAdapter(config) as adapter:
        tools = await adapter.list_tools()          # ← list_tools, not get_tools
        print("Available tools:", [t.name for t in tools])

        model = ChatGroq(model="openai/gpt-oss-120b")
        agent = create_agent(model, tools=tools)

        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": "What's (3+5) * 12?"}]}
        )
        print("Response:", response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())