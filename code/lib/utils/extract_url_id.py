def extract_url_id(url) -> str:
    """Extracts the id from a
    url like https://dev.i-learn.be/learningtracks/1
    """
    if url.endswith('/'):
        url = url[:-1]
    return url.split('/')[-1]
