"""Functions for working with URLs."""

from urllib.parse import quote, urlparse


def decode_url_braces(url: str) -> str:
    """Decodes curly braces in a URL string.

    This allows for arbitrary parameters to be passed in URL strings, as specified in some Algorand standards.
    For example, ARC-3 asset URLs may contain the string '{id}', which clients must replace with the asset ID in decimal form.

    Args:
        url (str): The URL string to decode.

    Returns:
        str: The decoded URL string.
    """
    parsed_url = urlparse(url)
    decoded_path = parsed_url.path.replace(quote("{"), "{").replace(quote("}"), "}")
    decoded_url = parsed_url._replace(path=decoded_path).geturl()
    return decoded_url
