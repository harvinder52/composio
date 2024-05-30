# Initial Setup

Set up the basic SDK and then head over to `local_tools`.

# How to Create a Local Tool

It is fairly easy to create a local tool. Follow the steps below to create a local tool. There are also example codes, and you can refer to `./webtools` for reference.

## Step 1: Create a New Folder

1. Create a new folder for your local tool.
2. Create two files: `__init__.py` and `<toolname>.py`, where `<toolname>` is the name of the tool you are creating. Keep in mind that the tool name must be in lowercase.

## Step 2: Basic Imports

In `<toolname>.py`, start with these basic imports:

```python
from pydantic import BaseModel, Field
from composio.local_tools.tool import Tool
from ..action import Action
```

## Step 3: Define Actions

Each tool can have multiple actions, and each action has three classes:

1. **Request Schema**: The schema for the objects that the action requires to perform.
2. **Response Schema**: The schema for the output you get.
3. **Execute Function**: The actual function that runs the action.

Here is how you write each one of them:

### Request Schema

Example:

```python
class ScrapeWebsiteToolRequest(BaseModel):
    website_url: str = Field(..., description="Mandatory website URL to read the file")
```

Define the request schema class. You can have multiple objects in the same format as the above one. Just define the variable, its type, and its properties. Follow the standard Pydantic rules; the three dots `...` mean that the field is required. The object can be a `str`, `int`, or any other datatype. The `description` is important as it helps the agent understand what to enter in the field.

If the action doesn't require any inputs, you can just use `pass` in this function, but it still needs to be defined.

### Response Schema

Most of the time, you can define it as a simple output variable, but if you need the output in a specific structured format, you can define the structure here.

Example:

```python
class ScrapeWebsiteToolResponse(BaseModel):
    website_content: str = Field(..., description="The content of the website")
```

### Execute Action Class

This class must have an `execute` function. This is crucial as naming it anything else may lead to errors.

Example:

```python
class ScrapeWebsiteTool(Action):
    """
    Scrape contents of a website
    """

    _display_name = "Scrape a website"
    _request_schema = ScrapeWebsiteToolRequest
    _response_schema = ScrapeWebsiteToolResponse
    _tags = ["Webbrowser"]
    _tool_name = "webtool"

    def execute(self, request: ScrapeWebsiteToolRequest, authorization_data: dict = {}):
        """Scrape the website and return the content"""
        url = request.website_url
        try:
            # Adding headers to mimic a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            req = Request(url, headers=headers)
            # Adding SSL context to handle CERTIFICATE_VERIFY_FAILED error
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            response = urlopen(req, context=context)
            html = response.read().decode('utf-8')
            soup = BeautifulSoup(html, 'html.parser')
            return ScrapeWebsiteToolResponse(website_content=str(soup))
        except Exception as e:
            return ScrapeWebsiteToolResponse(website_content=f"Error scraping website: {e}")
```

After defining the class, add the following code:

```python
_display_name = "Scrape a website"
_request_schema = ScrapeWebsiteToolRequest
_response_schema = ScrapeWebsiteToolResponse
_tags = ["Webbrowser"]
_tool_name = "webtool"
```

Ensure the `_tool_name` matches the file name. Then define your `execute` function, write the necessary Python code to perform the action, and return the data, which will be received by the response schema and parsed, finally reaching your agent.

You can have multiple actions in the same format with different names.

## Step 4: Register Actions

Now that you have made your actions, ensure the rest of the SDK receives them. At the end of the file, add a class that passes all the actions and triggers you have created.

Example:

```python
class WebTool(Tool):
    """Web Tools"""

    def actions(self) -> list:
        return [ScrapeWebsiteTool, ScrapeWebsiteElementTool]
```

Change the class name (`WebTool` in the example) and return an array of all the actions you have created (`ScrapeWebsiteTool` and `ScrapeWebsiteElementTool` in the example).

## Step 5: Update `__init__.py`

Go to the `__init__.py` file you created before and add a line of code importing the tool class you created in the previous step. Save the file.

# Testing

Now that you have created a local tool, you can test it by saving this tool and updating it in the enums. Run this command in your terminal:

```bash
composio apps update
```

If you encounter any errors, resolve them and update the code.

You can then simply import the tool as a normal tool in your agent or any other file you are using.
