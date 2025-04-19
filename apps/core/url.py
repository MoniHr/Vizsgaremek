from urllib.parse import urlparse


def get_base_url_from_request(request) -> str:
    url = urlparse(request.build_absolute_uri())
    url_str = f"{url.scheme}://{url.netloc}"
    return url_str
