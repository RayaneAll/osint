import re
import validators
from ipaddress import ip_address, ip_network, AddressValueError
from urllib.parse import urlparse


def validate_ip(ip):
    """
    Validate IPv4 or IPv6 address.

    Args:
        ip: IP address string

    Returns:
        Boolean indicating validity
    """
    try:
        ip_address(ip)
        return True
    except (AddressValueError, ValueError):
        return False


def validate_cidr(cidr):
    """
    Validate CIDR notation.

    Args:
        cidr: CIDR string (e.g., '192.168.1.0/24')

    Returns:
        Boolean indicating validity
    """
    try:
        ip_network(cidr, strict=False)
        return True
    except (AddressValueError, ValueError):
        return False


def validate_domain(domain):
    """
    Validate domain name format.

    Args:
        domain: Domain name string

    Returns:
        Boolean indicating validity
    """
    if not domain or len(domain) > 255:
        return False

    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*'
        r'[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$'
    )

    return bool(domain_regex.match(domain))


def validate_hash(hash_value, hash_type=None):
    """
    Validate hash format (MD5, SHA1, SHA256).

    Args:
        hash_value: Hash string
        hash_type: Expected hash type ('md5', 'sha1', 'sha256') or None for auto-detect

    Returns:
        Boolean indicating validity
    """
    if not hash_value:
        return False

    hash_patterns = {
        'md5': (32, r'^[a-fA-F0-9]{32}$'),
        'sha1': (40, r'^[a-fA-F0-9]{40}$'),
        'sha256': (64, r'^[a-fA-F0-9]{64}$')
    }

    if hash_type:
        if hash_type.lower() not in hash_patterns:
            return False
        length, pattern = hash_patterns[hash_type.lower()]
        return len(hash_value) == length and bool(re.match(pattern, hash_value))

    for length, pattern in hash_patterns.values():
        if len(hash_value) == length and re.match(pattern, hash_value):
            return True

    return False


def validate_url(url):
    """
    Validate URL format.

    Args:
        url: URL string

    Returns:
        Boolean indicating validity
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def detect_hash_type(hash_value):
    """
    Detect hash type based on length.

    Args:
        hash_value: Hash string

    Returns:
        Hash type string ('md5', 'sha1', 'sha256') or None
    """
    length = len(hash_value)
    hash_types = {
        32: 'md5',
        40: 'sha1',
        64: 'sha256'
    }
    return hash_types.get(length)
