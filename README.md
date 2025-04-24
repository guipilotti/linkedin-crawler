
# 🤖 LinkedIn Feed Crawler for PostsFeed (Render-ready)

This project is a lightweight crawler that uses `Selenium` to extract posts from LinkedIn based on a custom search and automatically fills a Google Sheet with the results.

## Features
- Headless scraping of LinkedIn posts
- Extracts text, author, timestamp and link
- Skips duplicates before writing
- Runs on Render via scheduled jobs

## Setup
1. Upload `main.py` and `requirements.txt` to a GitHub repo
2. Add `credentials.json` (Google Sheets API key)
3. Set environment variable in Render:
   - `LI_AT`: Your LinkedIn session cookie

## Cron Suggestion
- Run daily at 9am: `@daily`

## Output
Writes to your Google Sheet (`Linkedin_Assistant` > `PostsFeed`) with the structure:
- Texto do Post
- Link do Post
- Autor
- Data do Post
- Status
