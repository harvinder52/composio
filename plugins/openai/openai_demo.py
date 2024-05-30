"""
OpenAI demo.
"""

import dotenv
from composio_openai import App, ComposioToolSet
from openai import OpenAI


# Load environment variables from .env
dotenv.load_dotenv()

# Initialize tools.
composio_toolset = ComposioToolSet()

# Define task.
task = "what is the page about give a short summary of whatever is happening on this site 'https://writings.stephenwolfram.com/2021/03/what-is-consciousness-some-new-perspectives-from-our-physics-project/' keep it as short as possible"

# Get GitHub tools that are pre-configured
tools = composio_toolset.get_tools(apps=[App.WEBTOOL])

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
