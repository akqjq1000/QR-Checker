from web_screenshot import build_capture_filename


def test_build_capture_filename_uses_url_name():
    name = build_capture_filename("https://example.com/path/page?x=1")

    assert name.endswith(".png")
    assert "example.com" in name
    assert "page" in name
    assert len(name) > 10
