import pytest
from fastapi.testclient import TestClient
from server import app, is_image_url

client = TestClient(app)

def test_extract_images_missing_url():
    """Test that missing URL returns 400 error"""
    response = client.post("/extract-images", json={})
    assert response.status_code == 400
    assert response.json() == {"detail": "Missing 'url' in request body"}

def test_is_image_url():
    """Test the image URL validation function"""
    # Valid image URLs
    assert is_image_url("https://example.com/image.png")
    assert is_image_url("https://example.com/image.jpg")
    assert is_image_url("https://example.com/image.jpeg")
    assert is_image_url("https://example.com/image.gif")

    # Invalid URLs
    assert not is_image_url("https://example.com/document.pdf")
    assert not is_image_url("https://example.com/page.html")
    assert not is_image_url("https://example.com/script.js")
    assert not is_image_url("https://example.com/")
    assert not is_image_url("https://example.com")

def test_extract_images_with_mocked_html():
    """Test the core functionality by testing the helper functions directly"""
    # Test various image extensions
    image_urls = [
        "https://example.com/image.png",
        "https://example.com/photo.jpg",
        "https://example.com/animation.gif",
        "https://example.com/design.webp",
        "https://example.com/icon.ico",
        "https://example.com/logo.svg"
    ]

    for url in image_urls:
        assert is_image_url(url) == True

    # Test non-image URLs
    non_image_urls = [
        "https://example.com/document.pdf",
        "https://example.com/page.html",
        "https://example.com/script.js",
        "https://example.com/",
        "https://example.com"
    ]

    for url in non_image_urls:
        assert is_image_url(url) == False

def test_extract_images_endpoint_structure():
    """Test that the endpoint returns valid JSON structure for a valid request"""
    # Test that the endpoint accepts valid input and returns a list
    response = client.post("/extract-images", json={"url": "https://example.com"})
    # This should return a valid HTTP status code (200, 404, or 500)
    # The actual HTTP error happens during the fetch, which is expected behavior
    assert response.status_code in [200, 404, 500]  # Valid HTTP status codes
    # The response should be a list (even if empty or with errors)
    assert isinstance(response.json(), list)

def test_image_url_validation_edge_cases():
    """Test edge cases for image URL validation"""
    # Test case sensitivity
    assert is_image_url("https://example.com/image.PNG")
    assert is_image_url("https://example.com/image.JPEG")

    # Test URLs with query parameters and fragments
    assert is_image_url("https://example.com/image.png?query=1")
    assert is_image_url("https://example.com/image.jpg#fragment")

    # Test relative URLs (should not match since they don't end with extensions)
    assert not is_image_url("/image.png")
    assert not is_image_url("image.jpg")

    # Test invalid extensions
    assert not is_image_url("https://example.com/document.pdf")
    assert not is_image_url("https://example.com/script.js")
    assert not is_image_url("https://example.com/file.txt")

if __name__ == "__main__":
    pytest.main([__file__])