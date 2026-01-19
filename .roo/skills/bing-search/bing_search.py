#!/usr/bin/env python3
"""
Bing Search Skill - Minimal script for searching Bing and returning structured results.
"""

import sys
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


@dataclass
class SearchResult:
    """Represents a single search result from Bing."""
    title: str
    url: str
    snippet: str


class BingSearchSkill:
    """A skill for searching Bing and returning structured markdown results."""
    
    BASE_URL = "https://www.bing.com/search"
    # Note: Accept-Language header is excluded when using setLang parameter
    # to avoid conflicts. See: https://docs.microsoft.com/en-us/bing/search-apis/
    BASE_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    
    def __init__(self, max_results: int = 10, timeout: int = 10, market: str = "en-US", language: str = "en"):
        """
        Initialize the Bing Search Skill.
        
        Args:
            max_results: Maximum number of search results to return (default: 10)
            timeout: Request timeout in seconds (default: 10)
            market: Market code for localization in format <language>-<region> (default: "en-US")
                    Examples: "en-US", "en-GB", "de-DE", "fr-FR", "he-IL"
            language: Language code for results in ISO 639-1 format (default: "en")
                      Examples: "en", "de", "fr", "he"
        """
        self.max_results = max_results
        self.timeout = timeout
        self.market = market
        self.language = language
        self._last_error = None
    
    def _build_search_url(self, query: str) -> str:
        """Build the Bing search URL with localization parameters."""
        encoded_query = quote_plus(query)
        return f"{self.BASE_URL}?q={encoded_query}&mkt={self.market}&setLang={self.language}"
    
    def _fetch_html(self, url: str) -> Optional[str]:
        try:
            response = requests.get(
                url,
                headers=self.BASE_HEADERS,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self._last_error = str(e)
            return None
    
    def _parse_results(self, html: str) -> List[SearchResult]:
        results = []
        soup = BeautifulSoup(html, "html.parser")
        
        search_results = soup.find_all("li", class_="b_algo")
        
        for item in search_results[:self.max_results]:
            try:
                title_elem = item.find("h2")
                if not title_elem:
                    continue
                    
                link_elem = title_elem.find("a")
                if not link_elem:
                    continue
                
                title = link_elem.get_text(strip=True)
                url = link_elem.get("href", "")
                
                snippet = ""
                caption_elem = item.find("div", class_="b_caption")
                if caption_elem:
                    p_elem = caption_elem.find("p")
                    if p_elem:
                        snippet = p_elem.get_text(strip=True)
                
                if title and url:
                    results.append(SearchResult(
                        title=title,
                        url=url,
                        snippet=snippet
                    ))
            except Exception:
                continue
        
        return results
    
    def _format_as_markdown(self, query: str, results: List[SearchResult], error: Optional[str] = None) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if error:
            return f"""## Bing Search Results for: {query}

**Error:** Unable to fetch search results.

**Details:** {error}

---
*Search attempted at {timestamp}*
"""
        
        if not results:
            return f"""## Bing Search Results for: {query}

No results found for this query.

---
*Search completed at {timestamp} | 0 results found*
"""
        
        lines = [f"## Bing Search Results for: {query}", ""]
        
        for i, result in enumerate(results, 1):
            lines.append(f"### {i}. {result.title}")
            lines.append(f"**URL:** {result.url}")
            if result.snippet:
                lines.append(f"**Snippet:** {result.snippet}")
            lines.append("")
            lines.append("---")
            lines.append("")
        
        lines.append(f"*Search completed at {timestamp} | {len(results)} results found*")
        
        return "\n".join(lines)
    
    def search(self, query: str) -> str:
        self._last_error = None
        
        url = self._build_search_url(query)
        html = self._fetch_html(url)
        
        if html is None:
            return self._format_as_markdown(query, [], error=self._last_error)
        
        try:
            results = self._parse_results(html)
        except Exception as e:
            return self._format_as_markdown(query, [], error=f"Failed to parse results: {e}")
        
        return self._format_as_markdown(query, results)


def bing_search(query: str, max_results: int = 10, market: str = "en-US", language: str = "en") -> str:
    """
    Convenience function to search Bing.
    
    Args:
        query: The search query string
        max_results: Maximum number of search results to return (default: 10)
        market: Market code for localization in format <language>-<region> (default: "en-US")
                Examples: "en-US", "en-GB", "de-DE", "fr-FR", "he-IL"
        language: Language code for results in ISO 639-1 format (default: "en")
                  Examples: "en", "de", "fr", "he"
    
    Returns:
        Markdown-formatted search results
    """
    skill = BingSearchSkill(max_results=max_results, market=market, language=language)
    return skill.search(query)


def _parse_args():
    """Parse command line arguments."""
    import argparse
    parser = argparse.ArgumentParser(
        description="Search Bing and return structured markdown results.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python bing_search.py Python tutorials
  python bing_search.py --market en-GB "weather in London"
  python bing_search.py --market de-DE --language de "Berlin Nachrichten"
  python bing_search.py --market he-IL --language he "חדשות ישראל"
        """
    )
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument(
        "--market", "-m",
        default="en-US",
        help="Market code for localization (default: en-US). Examples: en-US, en-GB, de-DE, fr-FR, he-IL"
    )
    parser.add_argument(
        "--language", "-l",
        default="en",
        help="Language code for results in ISO 639-1 format (default: en). Examples: en, de, fr, he"
    )
    parser.add_argument(
        "--max-results", "-n",
        type=int,
        default=10,
        help="Maximum number of results to return (default: 10)"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    query = " ".join(args.query)
    print(bing_search(query, max_results=args.max_results, market=args.market, language=args.language))
