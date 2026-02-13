import asyncio
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re

app = FastAPI(title="Image Extractor API")

# Regex pattern to strictly match common image extensions
IMAGE_PATTERN = re.compile(r'.*\.(?:png|jpe?g|gif|webp|bmp|ico|svg)$', re.IGNORECASE)

def is_image_url(url: str) -> bool:
    """Check if the URL ends with a common image extension."""
    return bool(IMAGE_PATTERN.match(url))

@app.post("/extract-images")
async def extract_images(body: dict):
    """
    Accepts a JSON payload {'url': 'https://example.com'},
    fetches the page, and returns a list of absolute image URLs.
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
        for img_tag in soup.find_all("img"):
            src = img_tag.get("src")
            if src:
                # Join relative URLs with the base URL
                absolute_url = urljoin(target_url, src)
                if is_image_url(absolute_url):
                    found_urls.add(absolute_url)

        # 2. Look for background images in inline styles (Optional but useful)
        for tag in soup.find_all(style=True):
            style_attr = tag.get("style", "")
            # Look for url('...') or url("...")
            urls_in_style = re.findall(r'url\([\'"]?(.*?\.(?:png|jpe?g|gif|webp))[\'"]?\)', style_attr, re.IGNORECASE)
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
    uvicorn.run(app, host="0.0.0.0", port=8000)
