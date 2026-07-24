import os
import requests

from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv
from rich import print
from bs4 import BeautifulSoup

load_dotenv()

print("TAVILY KEY:", os.getenv("TAVILY_API_KEY"))

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str) -> str:
    print("=" * 60)
    print("Searching:", query)

    try:
        results = tavily.search(query=query, max_results=5)

        print("Results:", len(results["results"]))

        out = []

        for r in results["results"]:
            out.append(
                f"Title: {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Snippet: {r['content'][:300]}"
            )

        print("Finished search")
        return "\n----\n".join(out)

    except Exception as e:
        print("ERROR:", e)
        return ""


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""

    try:
        resp = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator=" ", strip=True)[:3000]

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
