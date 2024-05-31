from datetime import datetime

import dotenv
from composio_openai import App, ComposioToolSet
from openai import OpenAI


# Load environment variables from .env
dotenv.load_dotenv()

# Initialize tools.
openai_client = OpenAI()
composio_toolset = ComposioToolSet()

# Retrieve actions
tools = composio_toolset.get_acti(apps=[Action])

# Setup openai assistant
assistant_instruction = (
    "You are a super intelligent personal assistant."
    + "You have been given a set of tools that you are supposed to choose from."
    + "You decide the right tool and execute it."
)
# Prepare assistant
assistant = openai_client.beta.assistants.create(
    name="Personal Assistant",
    instructions=assistant_instruction,
    model="gpt-4-turbo-preview",
    tools=tools,  # type: ignore
)

# Give a task to execute via Openai Assistants
my_task = (
    f"scrape this page and then do a semantic search to find all the relevent info related to neural networks. the url is  'https://www.jeremykun.com/main-content/' delete the instance after you are done "
)

# create a thread
thread = openai_client.beta.threads.create()
print("Thread ID: ", thread.id)
print("Assistant ID: ", assistant.id)

# start the asssitant with my task
message = openai_client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=my_task,
)

# Execute Agent with intergrations
run = openai_client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

# Execute function calls
run_after_tool_calls = composio_toolset.wait_and_handle_assistant_tool_calls(
    client=openai_client,
    run=run,
    thread=thread,
)

print(run_after_tool_calls)
