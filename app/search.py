import os
import requests
from dotenv import load_dotenv


load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")


def search_web(query, num_results=10):
    """
    Search the web using the Serper API.

    Args:
        query (str): Name, username, or search query.
        num_results (int): Number of results to retrieve.

    Returns:
        list: Search results containing title, URL, and snippet.
    """

    if not SERPER_API_KEY:
        print("Error: SERPER_API_KEY is missing from .env")
        return []

    url = "https://google.serper.dev/search"

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "q": query,
        "num": num_results
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()

    except requests.RequestException as error:
        print(f"Search request failed: {error}")
        return []

    data = response.json()

    results = []

    for result in data.get("organic", []):
        results.append({
            "title": result.get("title", ""),
            "url": result.get("link", ""),
            "snippet": result.get("snippet", "")
        })

    return results