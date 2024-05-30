from pydantic import BaseModel, Field
import ssl
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from composio.local_tools.tool import Tool
from ..action import Action


class ScrapeWebsiteToolRequest(BaseModel):
    website_url: str = Field(..., description="Mandatory website url to read the file")

class ScrapeWebsiteToolResponse(BaseModel):
    website_content: str = Field(..., description="The content of the website")

class ScrapeWebsiteTool(Action):
    """
    Scrape contents of a website
    """

    _display_name = "Scrape a website"
    _request_schema = ScrapeWebsiteToolRequest
    _response_schema = ScrapeWebsiteToolResponse
    _tags = ["Webbrowser"]
    _tool_name = "webtool"
 
                
    def execute(self, request: ScrapeWebsiteToolRequest, authorisation_data: dict = {}):
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

class ScrapeWebsiteElementToolRequest(BaseModel):
    website_url: str = Field(..., description="Mandatory website url to read the file")
    element_selector: str = Field(..., description="CSS selector for the element to scrape")

class ScrapeWebsiteElementToolResponse(BaseModel):
    element_content: str = Field(..., description="The content of the selected element")


class ScrapeWebsiteElementTool(Action):
    """
    Scrame website element
    """
    _display_name = "Scrape a website element"
    _request_schema = ScrapeWebsiteElementToolRequest
    _response_schema = ScrapeWebsiteElementToolResponse
    _tags = ["Webbrowser"]
    _tool_name = "webtool"
    
    def execute(self, request: ScrapeWebsiteElementToolRequest , authorisation_data: dict = {}):
        """Scrape a specific element from the website and return its content"""
        url = request.website_url
        selector = request.element_selector
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
            element = soup.select_one(selector)
            if element:
                return ScrapeWebsiteElementToolResponse(element_content=str(element))
            else:
                return ScrapeWebsiteElementToolResponse(element_content="Element not found")
        except Exception as e:
            return ScrapeWebsiteElementToolResponse(element_content=f"Error scraping element: {e}")

class WebTool(Tool):
    """Web Tools"""
    
    def actions(self) -> list:
        return [ScrapeWebsiteTool, ScrapeWebsiteElementTool]

