"""
OpenAI demo.
"""

import dotenv
from composio_openai import App, ComposioToolSet
from openai import OpenAI


# Load environment variables from .env
dotenv.load_dotenv()

# Initialize tools.
openai_client = OpenAI()
composio_toolset = ComposioToolSet()

# Define task.
task = "scrape this page and then do a semantic search to find all the relevent info related to neural networks. the url is  'https://www.jeremykun.com/main-content/' delete the instance after you are done"

# Get GitHub tools that are pre-configured
tools = composio_toolset.get_tools(apps=[App.WEBTOOL, App.RAGTOOLACTIONS])

# Get response from the LLM 
response = openai_client.chat.completions.create(
    model="gpt-4-turbo-preview",
    tools=tools,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": task},
    ],
)
print(response)

# Execute the function calls.
result = composio_toolset.handle_tool_calls(response)
print(result)
