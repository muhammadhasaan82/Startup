````markdown
# 022 - Selenium SPA Scraper and Safe Reindexing

**Date:** 2026-01-31
**Developer:** AI Assistant

## Summary

Upgraded the chatbot scraper to use Selenium for JavaScript-rendered SPA pages and added safe reindexing to avoid clearing the vector store before a successful scrape.

## Changes Made

### 1. Selenium-based SPA Scraping
**Problem:** Requests/BeautifulSoup cannot render React SPA content in production.
**Solution:** Implemented Selenium headless Chrome crawling with dynamic link discovery.

- **Updated:** `Chatbot/scraper.py`
  - Uses Selenium headless Chrome to render pages.
  - Dynamically discovers internal links from rendered HTML.

### 2. Safe Reindexing (No Downtime)
**Problem:** Clearing the vector store before scraping causes downtime if scraping fails.
**Solution:** Scrape first, then clear and reindex only on success.

- **Updated:** `Chatbot/main.py`
  - `/reindex` now scrapes first and only clears on success.

### 3. Dependency Updates
- **Updated:** `Chatbot/requirements.txt`
  - Added `selenium` and `webdriver-manager`.
  - Removed `playwright`.

## Verification

- Scraper now renders SPA content and extracts text from fully loaded pages.
- Reindex endpoint maintains existing data if scraping fails.

## Git Commits

```
fix(chatbot): use selenium for SPA scraping and safe reindex
```
````
