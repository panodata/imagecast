import re

from fastapi.testclient import TestClient

from imagecast.api import app, Settings, get_settings

client = TestClient(app)


def get_settings_override():
    """
    Override settings to permit access to iana.org and unsplash.com.
    """
    return Settings(allowed_hosts=["www.iana.org", "unsplash.com"])


app.dependency_overrides[get_settings] = get_settings_override


def test_api_index():
    """
    Verify HTML index page rendering works.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert re.match(r".*<title>imagecast [\d.]+</title>.*", response.text, re.DOTALL)


def test_api_unsplash_converge(caplog):
    """
    Verify image management works.
    """
    query_params = {
        "uri": "https://unsplash.com/photos/WvdKljW55rM/download?force=true",
        "monochrome": "80",
        "crop": "850,1925,-950,-900",
        "width": "640",
    }
    response = client.get("/", params=query_params)

    # Verify log output.
    assert "Acquiring image from https://unsplash.com/photos/WvdKljW55rM/download?force=true" in caplog.messages

    # Verify content output.
    assert response.status_code == 200
    assert response.content.startswith(b"\xff\xd8\xff\xe0\x00\x10JFIF")


def test_api_html_acquire(caplog):
    """
    Verify HTML DOM element acquisition works.
    """
    query_params = {
        "uri": "https://www.iana.org/help/example-domains",
        "element": "#logo",
    }
    response = client.get("/", params=query_params)

    # Verify log output.
    assert "Acquiring image from https://www.iana.org/help/example-domains" in caplog.messages

    # Verify content output.
    assert response.status_code == 200
    assert response.content.startswith(b"\x89PNG\r\n\x1a")
