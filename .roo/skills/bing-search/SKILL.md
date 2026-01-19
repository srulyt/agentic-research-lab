---
name: bing-search
description: Search Bing for web results when users need current information from the web. Returns structured markdown with titles, URLs, and snippets for each result. Use this skill when users ask for web searches, need to find information online, or want to look up current topics. Supports localization via market and language parameters.
---

# Bing Search Skill

This skill allows you to search Bing and retrieve structured web results with localization support.

## Usage

To perform a Bing search, execute the bundled Python script `bing_search.py` located in this skill directory with the search query as command-line arguments.

### Command Format

```bash
python .roo/skills/bing-search/bing_search.py [OPTIONS] <search query>
```

### Options

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--market` | `-m` | `en-US` | Market code for localization in `<language>-<region>` format |
| `--language` | `-l` | `en` | Language code for results in ISO 639-1 format |
| `--max-results` | `-n` | `10` | Maximum number of results to return |

### Localization Parameters

**Market (`--market`, `-m`):** Controls the geographic region for search results. Format: `<language>-<region>`
- `en-US` - English, United States (default)
- `en-GB` - English, United Kingdom
- `de-DE` - German, Germany
- `fr-FR` - French, France
- `he-IL` - Hebrew, Israel
- `es-ES` - Spanish, Spain
- `ja-JP` - Japanese, Japan

**Language (`--language`, `-l`):** Controls the language of the results. Format: ISO 639-1 two-letter code
- `en` - English (default)
- `de` - German
- `fr` - French
- `he` - Hebrew
- `es` - Spanish
- `ja` - Japanese

### Examples

1. Search for Python tutorials (default English/US):
   ```bash
   python .roo/skills/bing-search/bing_search.py Python tutorials for beginners
   ```

2. Search in UK market:
   ```bash
   python .roo/skills/bing-search/bing_search.py --market en-GB "weather in London"
   ```

3. Search in German with German results:
   ```bash
   python .roo/skills/bing-search/bing_search.py --market de-DE --language de "Berlin Nachrichten"
   ```

4. Search in Hebrew:
   ```bash
   python .roo/skills/bing-search/bing_search.py --market he-IL --language he "חדשות ישראל"
   ```

5. Search with limited results:
   ```bash
   python .roo/skills/bing-search/bing_search.py --max-results 5 machine learning best practices
   ```

## Output

The script returns markdown-formatted results containing:
- Search query header
- Numbered results with:
  - Title
  - URL
  - Snippet (description)
- Timestamp and result count

## Requirements

The script requires `requests` and `beautifulsoup4` packages. If not installed, run:
```bash
pip install requests beautifulsoup4
```

## Notes

- The script fetches up to 10 results by default
- Results are scraped from Bing's web search page
- If the search fails, an error message will be returned in the output
- Localization uses Bing's `mkt` (market) and `setLang` (language) query parameters
- The `Accept-Language` header is intentionally excluded to avoid conflicts with `setLang`
