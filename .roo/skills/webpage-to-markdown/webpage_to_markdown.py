#!/usr/bin/env python3
"""
Webpage to Markdown Converter

Fetches a webpage and extracts the main content as clean markdown.
Preserves headings, text styling, lists, links, and code blocks.
"""

import sys
import re
from urllib.parse import urlparse

# Check for Brotli support at runtime
BROTLI_AVAILABLE = False
try:
    import brotli
    BROTLI_AVAILABLE = True
except ImportError:
    try:
        import brotlicffi
        BROTLI_AVAILABLE = True
    except ImportError:
        pass

try:
    import requests
except ImportError:
    print("Error: 'requests' package is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: 'beautifulsoup4' package is required. Install with: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

try:
    import html2text
except ImportError:
    print("Error: 'html2text' package is required. Install with: pip install html2text", file=sys.stderr)
    sys.exit(1)


# Elements to remove from the page (non-content elements)
ELEMENTS_TO_REMOVE = [
    'script', 'style', 'nav', 'header', 'footer', 'aside',
    'iframe', 'noscript', 'svg', 'form', 'button', 'input',
    'select', 'textarea', 'advertisement', 'ads', 'sidebar',
    'menu', 'toolbar', 'social', 'share', 'comment', 'comments',
    'related', 'recommended', 'popup', 'modal', 'cookie', 'banner'
]

# Classes and IDs that typically indicate non-content areas
NON_CONTENT_PATTERNS = [
    r'nav', r'header', r'footer', r'sidebar', r'aside', r'menu',
    r'advertisement', r'ads?[-_]?', r'social', r'share', r'comment',
    r'related', r'recommended', r'popup', r'modal', r'cookie',
    r'banner', r'promo', r'newsletter', r'subscribe', r'widget',
    r'breadcrumb', r'pagination', r'pager', r'toolbar', r'search'
]


def is_valid_url(url: str) -> bool:
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme in ('http', 'https'), result.netloc])
    except Exception:
        return False


def fetch_webpage(url: str) -> str:
    """Fetch webpage content with proper headers."""
    # Only advertise Brotli compression if the library is available
    accept_encoding = 'gzip, deflate, br' if BROTLI_AVAILABLE else 'gzip, deflate'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': accept_encoding,
        'Connection': 'keep-alive',
    }
    
    response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
    response.raise_for_status()
    
    # Try to detect encoding
    if response.encoding is None or response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding or 'utf-8'
    
    return response.text


def should_remove_element(element) -> bool:
    """Check if an element should be removed based on its attributes."""
    if not element.name:
        return False
    
    # Check element name
    if element.name.lower() in ELEMENTS_TO_REMOVE:
        return True
    
    # Check class and id attributes
    classes = element.get('class', [])
    if isinstance(classes, str):
        classes = [classes]
    element_id = element.get('id', '')
    
    # Combine all attributes to check
    attrs_to_check = ' '.join(classes + [element_id]).lower()
    
    for pattern in NON_CONTENT_PATTERNS:
        if re.search(pattern, attrs_to_check, re.IGNORECASE):
            return True
    
    # Check for hidden elements
    style = element.get('style', '')
    if 'display:none' in style.replace(' ', '').lower() or 'visibility:hidden' in style.replace(' ', '').lower():
        return True
    
    # Check aria-hidden
    if element.get('aria-hidden') == 'true':
        return True
    
    return False


def find_main_content(soup: BeautifulSoup) -> BeautifulSoup:
    """Find the main content area of the page."""
    # Priority order for finding main content
    content_selectors = [
        'article',
        'main',
        '[role="main"]',
        '[role="article"]',
        '.article',
        '.post',
        '.content',
        '.main-content',
        '.post-content',
        '.article-content',
        '.entry-content',
        '.page-content',
        '#content',
        '#main',
        '#article',
    ]
    
    # Try each selector in priority order
    for selector in content_selectors:
        content = soup.select_one(selector)
        if content and len(content.get_text(strip=True)) > 200:
            return content
    
    # Fallback: find the largest text block
    body = soup.find('body')
    if not body:
        return soup
    
    # Find all potential content containers
    candidates = body.find_all(['div', 'section', 'article'])
    
    if not candidates:
        return body
    
    # Score candidates by text length and content quality
    best_candidate = None
    best_score = 0
    
    for candidate in candidates:
        # Skip if it's a non-content element
        if should_remove_element(candidate):
            continue
        
        text = candidate.get_text(strip=True)
        text_length = len(text)
        
        # Count paragraphs as a quality indicator
        paragraphs = len(candidate.find_all('p'))
        
        # Calculate score
        score = text_length + (paragraphs * 100)
        
        if score > best_score:
            best_score = score
            best_candidate = candidate
    
    return best_candidate if best_candidate else body


def clean_html(soup: BeautifulSoup) -> BeautifulSoup:
    """Remove non-content elements from the soup."""
    # Remove unwanted elements by tag name
    for tag in ELEMENTS_TO_REMOVE:
        for element in soup.find_all(tag):
            element.decompose()
    
    # Remove elements based on class/id patterns
    for element in soup.find_all(True):
        if should_remove_element(element):
            element.decompose()
    
    # Remove empty elements (except for self-closing tags)
    for element in soup.find_all(True):
        if element.name not in ['br', 'hr', 'img', 'input', 'meta', 'link']:
            if not element.get_text(strip=True) and not element.find_all(['img', 'video', 'audio', 'iframe']):
                element.decompose()
    
    return soup


def convert_to_markdown(html_content: str) -> str:
    """Convert HTML to clean markdown."""
    # Configure html2text
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.ignore_emphasis = False
    converter.body_width = 0  # Don't wrap lines
    converter.unicode_snob = True  # Use unicode instead of ascii
    converter.skip_internal_links = True
    converter.inline_links = True
    converter.protect_links = True
    converter.ignore_tables = False
    converter.single_line_break = False
    converter.mark_code = True
    converter.wrap_links = False
    converter.wrap_list_items = False
    converter.pad_tables = True
    
    # Convert to markdown
    markdown = converter.handle(html_content)
    
    # Clean up the markdown
    markdown = clean_markdown(markdown)
    
    return markdown


def clean_markdown(text: str) -> str:
    """Clean up the converted markdown."""
    # Remove excessive blank lines (more than 2 consecutive)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove leading/trailing whitespace from lines while preserving structure
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Preserve indentation for code blocks and lists
        if line.startswith('    ') or line.startswith('\t') or line.startswith('```'):
            cleaned_lines.append(line.rstrip())
        else:
            cleaned_lines.append(line.strip())
    text = '\n'.join(cleaned_lines)
    
    # Fix common markdown issues
    # Remove excessive spaces before punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    # Fix broken links (newlines in link text)
    text = re.sub(r'\[([^\]]*)\n([^\]]*)\]', r'[\1 \2]', text)
    
    # Remove image alt text that's just "image" or empty
    text = re.sub(r'!\[\s*(image)?\s*\]\([^)]+\)', '', text, flags=re.IGNORECASE)
    
    # Clean up list formatting
    text = re.sub(r'(\n[*-]\s)', r'\n\1', text)
    
    # Remove trailing whitespace
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    
    # Remove leading/trailing blank lines
    text = text.strip()
    
    return text


def webpage_to_markdown(url: str) -> str:
    """Main function to convert a webpage to markdown."""
    # Validate URL
    if not is_valid_url(url):
        raise ValueError(f"Invalid URL format: {url}")
    
    # Fetch the webpage
    html_content = fetch_webpage(url)
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find main content area
    main_content = find_main_content(soup)
    
    if main_content is None:
        raise ValueError("Could not find main content on the page")
    
    # Clean the HTML
    cleaned_content = clean_html(main_content)
    
    # Convert to markdown
    markdown = convert_to_markdown(str(cleaned_content))
    
    if not markdown.strip():
        raise ValueError("No content could be extracted from the page")
    
    return markdown


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python webpage_to_markdown.py <URL>", file=sys.stderr)
        print("Example: python webpage_to_markdown.py https://example.com/article", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    
    try:
        markdown = webpage_to_markdown(url)
        print(markdown)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"Error: Request timed out while fetching {url}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {url}. Check your internet connection or the URL.", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code} - {e.response.reason}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch webpage - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
