import hashlib

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def shorten_url(long_url):
    """
    Shorten a long URL using SHA-256 hashing and base62 encoding.

    Parameters:
    - long_url (str): The original URL to be shortened.

    Returns:
    - str: The shortened URL.
    """
    url_hash = hashlib.sha256(long_url.encode()).hexdigest()[:8]
    url_id = int(url_hash, 16)
    short_url = encode_base62(url_id)
    return short_url

def encode_base62(num):
    """
    Encode a number in base62.

    Parameters:
    - num (int): The number to be encoded.

    Returns:
    - str: The base62-encoded string.
    """
    result = []
    while num > 0:
        num, remainder = divmod(num, 62)
        result.append(BASE62[remainder])
    return ''.join(result[::-1])
