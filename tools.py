import os
import requests

from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()

# Get Tavily API Key
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set. Please add it to your environment variables or Streamlit Secrets.")

# Initialize Tavily client
tavily = TavilyClient(api_key=TAVILY_API_KEY)


@tool
def web_search(query: str) -> str:
    """
    Search the web using the Tavily Search API and return formatted search results.
    """

    print("=" * 60)
    print(f"Searching: {query}")

    try:
        results = tavily.search(
            query=query,
            max_results=5
        )

        output = []

        for result in results.get("results", []):
            output.append(
                f"Title: {result.get('title', 'N/A')}\n"
                f"URL: {result.get('url', 'N/A')}\n"
                f"Snippet: {result.get('content', '')[:300]}"
            )

        print("Search completed successfully.")

        return "\n\n-----------------------------\n\n".join(output)

    except Exception as e:
        print(f"Tavily Error: {e}")
        return f"Search failed: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """
    Scrape a webpage and return its cleaned text content.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0.0.0 Safari/537.36"
                )
            },
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unwanted elements
        for tag in soup(["script", "style", "header", "footer", "nav", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
