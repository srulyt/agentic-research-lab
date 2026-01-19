---
name: webpage-to-markdown
description: Fetch a webpage and extract its main content as clean markdown. Preserves headings (h1-h6), text styling (bold, italic), lists (ordered and unordered), links, and code blocks. Use this skill when users need to read web articles, documentation pages, or any webpage content in a clean, readable format without ads, navigation, or other clutter.
---

# Webpage to Markdown

This skill fetches a webpage URL and extracts the main content, converting it to clean, readable markdown. It intelligently identifies the primary content area (article, main section, or largest content block) while stripping away navigation, advertisements, sidebars, footers, and other non-essential elements.

## Usage

When a user asks to fetch, read, or convert a webpage to markdown, use this skill to extract and display the content.

### Command Format

```bash
python .roo/skills/webpage-to-markdown/webpage_to_markdown.py <URL>
```

### Examples

**Fetch a documentation page:**
```bash
python .roo/skills/webpage-to-markdown/webpage_to_markdown.py https://docs.python.org/3/tutorial/introduction.html
```

**Read a blog article:**
```bash
python .roo/skills/webpage-to-markdown/webpage_to_markdown.py https://example.com/blog/article-title
```

**Extract content from a news article:**
```bash
python .roo/skills/webpage-to-markdown/webpage_to_markdown.py https://news.example.com/2024/01/story.html
```

## Output

The script outputs clean markdown to stdout, preserving:

- **Headings**: H1 through H6 converted to markdown heading syntax (`#` to `######`)
- **Text styling**: Bold (`**text**`) and italic (`*text*`)
- **Lists**: Both ordered (numbered) and unordered (bulleted) lists
- **Links**: Preserved as `[text](url)` format
- **Code**: Inline code and code blocks with proper markdown formatting
- **Paragraphs**: Proper spacing and line breaks

Elements that are stripped:
- Navigation menus
- Sidebars
- Footers and headers
- Advertisements
- Scripts and styles
- Comments and metadata

## Requirements

The following Python packages are required:

- `requests` - For fetching webpage content
- `beautifulsoup4` - For parsing and extracting HTML content
- `html2text` - For converting HTML to markdown

Install dependencies:
```bash
pip install requests beautifulsoup4 html2text
```

## Notes

### Limitations

- JavaScript-rendered content may not be captured (uses simple HTTP requests, not a browser)
- Some websites may block automated requests or require authentication
- Very complex layouts may not extract perfectly
- Images are converted to markdown image syntax but not downloaded

### Error Handling

The script handles common errors gracefully:

- **Invalid URL**: Returns an error message if the URL format is invalid
- **Network errors**: Reports connection failures, timeouts, or DNS resolution issues
- **HTTP errors**: Reports status codes for failed requests (404, 500, etc.)
- **Empty content**: Notifies when no main content could be extracted

### Tips

- For best results, provide direct URLs to article or content pages
- If content extraction is poor, the page may rely heavily on JavaScript
- Some paywalled content may not be accessible
