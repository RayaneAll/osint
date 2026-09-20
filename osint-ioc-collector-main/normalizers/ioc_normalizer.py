from urllib.parse import urlparse, urlunparse
from .validators import validate_ip, validate_domain, validate_hash, validate_url, detect_hash_type


def normalize_ip(ip):
    """
    Normalize IP address by stripping whitespace and validating format.

    Args:
        ip: IP address string

    Returns:
        Normalized IP address or None if invalid
    """
    if not ip:
        return None

    ip = ip.strip()

    if validate_ip(ip):
        return ip

    return None


def normalize_domain(domain):
    """
    Normalize domain by converting to lowercase, stripping protocol, and validating.

    Args:
        domain: Domain name string

    Returns:
        Normalized domain or None if invalid
    """
    if not domain:
        return None

    domain = domain.strip().lower()

    if domain.startswith(('http://', 'https://')):
        parsed = urlparse(domain)
        domain = parsed.netloc or parsed.path

    domain = domain.rstrip('.')

    if validate_domain(domain):
        return domain

    return None


def normalize_hash(hash_value):
    """
    Normalize hash by converting to uppercase and detecting type.

    Args:
        hash_value: Hash string

    Returns:
        Tuple of (normalized_hash, hash_type) or (None, None) if invalid
    """
    if not hash_value:
        return None, None

    hash_value = hash_value.strip().lower()

    hash_type = detect_hash_type(hash_value)

    if hash_type and validate_hash(hash_value, hash_type):
        return hash_value, hash_type

    return None, None


def normalize_url(url):
    """
    Normalize URL by parsing and validating.

    Args:
        url: URL string

    Returns:
        Normalized URL or None if invalid
    """
    if not url:
        return None

    url = url.strip()

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    if validate_url(url):
        parsed = urlparse(url)
        normalized = urlunparse((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
        return normalized

    return None


def detect_ioc_type(value):
    """
    Automatically detect IOC type from value.

    Args:
        value: IOC value string

    Returns:
        IOC type string ('ip', 'domain', 'hash', 'url') or None
    """
    if not value:
        return None

    value = value.strip()

    if validate_ip(value):
        return 'ip'

    if validate_url(value) and ('://' in value or value.count('/') > 1):
        return 'url'

    hash_value, hash_type = normalize_hash(value)
    if hash_type:
        return 'hash'

    if validate_domain(value):
        return 'domain'

    return None
