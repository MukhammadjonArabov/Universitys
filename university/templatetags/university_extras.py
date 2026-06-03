from urllib.parse import urlparse
from django import template

register = template.Library()

@register.filter
def domain(url: str) -> str:
    """Return a cleaned domain for display (e.g., nuu.uz).
    Adds http scheme if missing to allow correct parsing, strips www."""
    if not url:
        return ""
    url = str(url).strip()
    if not url:
        return ""
    if not url.startswith(('http://', 'https://')):
        url_to_parse = 'http://' + url
    else:
        url_to_parse = url
    try:
        p = urlparse(url_to_parse)
        host = p.netloc or p.path
    except Exception:
        host = url
    # Remove port if present
    if ':' in host:
        host = host.split(':')[0]
    # Strip www.
    if host.startswith('www.'):
        host = host[4:]
    return host
