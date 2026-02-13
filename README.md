# Image Extractor API

A FastAPI-based web service that extracts all image URLs from a given web page.

## Features

- Extracts image URLs from `<img>` tags
- Extracts background images from inline CSS styles
- Handles relative and absolute URLs
- Returns unique image URLs only
- Async HTTP requests for better performance
- Proper error handling and validation

## API Endpoint

### POST `/extract-images`

Extracts all image URLs from a given web page.

**Request Body:**

```json
{
  "url": "https://example.com"
}
```

**Response:**

```json
[
  "https://example.com/image1.jpg",
  "https://example.com/images/photo.png",
  "https://example.com/assets/background.webp"
]
```

## Requirements

- Python 3.7+
- FastAPI
- uvicorn
- httpx
- beautifulsoup4
- pytest (for testing)

## Installation

1. Clone the repository
2. Install dependencies:

   ```bash
   pip install fastapi uvicorn httpx beautifulsoup4 pytest
   ```

## Running the Server

```bash
python server.py
```

The server will start on `http://localhost:8000`.

## Running Tests

To run the tests:

```bash
pytest tests.py
```

## Usage Examples

### Using curl

```bash
curl -X POST "http://localhost:8000/extract-images" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### Using Python

```python
import requests

url = "http://localhost:8000/extract-images"
data = {"url": "https://example.com"}
response = requests.post(url, json=data)
images = response.json()
print(images)
```

## Error Handling

The API returns appropriate HTTP status codes:

- `400 Bad Request`: Missing URL in request body
- `404 Not Found`: URL not found
- `500 Internal Server Error`: General server error

## Supported Image Formats

The service recognizes these image extensions:

- `.png`
- `.jpg` / `.jpeg`
- `.gif`
- `.webp`
- `.bmp`
- `.ico`
- `.svg`

## License

This project is available under the MIT License.