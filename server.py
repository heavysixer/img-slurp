import asyncio
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re

app = FastAPI(title="Image Extractor API")

# Regex pattern to strictly match common image extensions with proper URL structure
# This pattern ensures URLs start with http:// or https:// and end with valid image extensions
IMAGE_PATTERN = re.compile(r'^https?://.*\.(?:png|jpe?g|gif|webp|ico|svg)$', re.IGNORECASE)

def is_image_url(url: str) -> bool:
    """
    Check if a URL points to an image file based on its extension.

    This function validates that:
    1. The URL is an absolute URL (starts with http:// or https://)
    2. The URL ends with a valid image extension (case-insensitive)
    3. Query parameters and fragments are properly handled

    Args:
        url (str): The URL to validate

    Returns:
        bool: True if the URL appears to point to an image file, False otherwise
    """
    # Remove query parameters and fragments before checking to avoid false negatives
    # For example: "https://example.com/image.png?query=1" becomes "https://example.com/image.png"
    clean_url = url.split('?')[0].split('#')[0]
    return bool(IMAGE_PATTERN.match(clean_url))

@app.post("/extract-images")
async def extract_images(body: dict):
    """
    Accepts a JSON payload {'url': 'https://example.com'},
    fetches the page, and returns a list of absolute image URLs.

    This endpoint:
    1. Validates that a URL is provided in the request body
    2. Fetches the HTML content from the provided URL
    3. Parses the HTML to find all image sources
    4. Handles both <img> tags and inline CSS background images
    5. Converts relative URLs to absolute URLs
    6. Filters results to only include valid image URLs
    7. Returns a list of unique image URLs

    Args:
        body (dict): JSON payload containing the 'url' key

    Returns:
        JSONResponse: List of absolute image URLs found on the page

    Raises:
        HTTPException: 400 if no URL is provided, 404 if URL fetch fails,
                      500 for network or internal server errors
    """
    target_url = body.get("url")

    if not target_url:
        raise HTTPException(status_code=400, detail="Missing 'url' in request body")

    try:
        # Use httpx for async HTTP requests
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(target_url, timeout=10.0)
            response.raise_for_status()
            
            html_content = response.text

        # Parse HTML
        soup = BeautifulSoup(html_content, "html.parser")
        
        found_urls = set() # Use a set to avoid duplicates

        # 1. Look for <img> tags
        # Extract all src attributes from img tags and convert to absolute URLs
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src")
            if src:
                # Join relative URLs with the base URL to create absolute URLs
                absolute_url = urljoin(target_url, src)
                if is_image_url(absolute_url):
                    found_urls.add(absolute_url)

        # 2. Look for background images in inline styles (Optional but useful)
        # Extract background images from CSS style attributes
        for tag in soup.find_all(style=True):
            style_attr = tag.get("style", "")
            # Look for url('...') or url("...") patterns in CSS
            # Note: This regex pattern is intentionally limited to common image extensions
            # to avoid false positives from other CSS properties
            urls_in_style = re.findall(r'url\([\'"]?(.*?\.(?:png|jpe?g|gif))[\'"]?\)', style_attr, re.IGNORECASE)
            for url in urls_in_style:
                absolute_url = urljoin(target_url, url)
                if is_image_url(absolute_url):
                    found_urls.add(absolute_url)

        # Convert set back to list for JSON serialization
        return JSONResponse(content=list(found_urls))

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to fetch URL: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# Run the server
if __name__ == "__main__":
    import uvicorn
    import argparse
    import os

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Image Extractor API Server")
    parser.add_argument("--port", "-p", type=int, default=8000, help="Port to run the server on (default: 8000)")
    args = parser.parse_args()

    # Allow port to be overridden by environment variable
    port = int(os.environ.get("PORT", args.port))

    uvicorn.run(app, host="0.0.0.0", port=port)
