import hashlib


base62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def shorten_url(long_url):
    # Generate a unique ID for the URL using its hash
    url_hash = hashlib.sha256(long_url.encode()).hexdigest()[:8]

    # Convert the hash to an integer
    url_id = int(url_hash, 16)

    # Encode the ID to base62
    short_url = encode_base62(url_id)
    return short_url

def encode_base62(num):
    result = []
    while num > 0:
        num, remainder = divmod(num, 62)
        result.append(base62[remainder])
    return ''.join(result[::-1])
