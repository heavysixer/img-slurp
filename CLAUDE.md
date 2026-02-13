# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based web service that extracts image URLs from web pages. The service accepts a URL as input, fetches the HTML content, and returns a list of absolute image URLs found in the page, including both `<img>` tags and background images in inline styles.

## Key Files

- `server.py`: Main FastAPI application with the `/extract-images` endpoint
- The application uses `httpx` for async HTTP requests and `BeautifulSoup` for HTML parsing

## Architecture

The service follows a simple REST API pattern using FastAPI:
- Single endpoint `/extract-images` that accepts POST requests with a JSON body containing a URL
- Uses async HTTP client for efficient requests
- Parses HTML with BeautifulSoup to extract image URLs
- Handles both direct `<img src="">` tags and inline CSS background images
- Implements proper error handling for network issues and HTTP errors

## Development Commands

To run the development server:
```
python server.py
```

The server will start on port 8000.

To test the API:
```
curl -X POST "http://localhost:8000/extract-images" -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
```

## Dependencies

The application requires:
- FastAPI
- uvicorn (for running the server)
- httpx (for async HTTP requests)
- beautifulsoup4 (for HTML parsing)

## Testing

The application has basic error handling for:
- Missing URL in request body
- HTTP status errors
- Network errors
- General exceptions

No unit tests are included in this codebase, but the API endpoint can be tested manually or with tools like curl or Postman.