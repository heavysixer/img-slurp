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

You can specify a custom port using the `--port` flag:

```bash
python server.py --port 8080
```

Or by setting the `PORT` environment variable:

```bash
PORT=8080 python server.py
```

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

### Using JavaScript (Fetch API)

```javascript
async function extractImages(url) {
  try {
    const response = await fetch('http://localhost:8000/extract-images', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const images = await response.json();
    console.log('Found images:', images);
    return images;
  } catch (error) {
    console.error('Error extracting images:', error);
  }
}

// Usage
extractImages('https://example.com');
```

### Using JavaScript (XMLHttpRequest)

```javascript
function extractImagesXHR(url) {
  const xhr = new XMLHttpRequest();
  xhr.open('POST', 'http://localhost:8000/extract-images', true);
  xhr.setRequestHeader('Content-Type', 'application/json');

  xhr.onreadystatechange = function() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        const images = JSON.parse(xhr.responseText);
        console.log('Found images:', images);
      } else {
        console.error('Error:', xhr.status, xhr.statusText);
      }
    }
  };

  const data = JSON.stringify({ url: url });
  xhr.send(data);
}

// Usage
extractImagesXHR('https://example.com');
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

## License

This project is available under the MIT License.
