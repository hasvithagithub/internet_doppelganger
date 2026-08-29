from urllib.parse import urlparse


SUPPORTED_PLATFORMS = {
    "github.com": "GitHub",
    "linkedin.com": "LinkedIn",
    "kaggle.com": "Kaggle",
    "medium.com": "Medium",
    "dev.to": "Dev.to",
}


def identify_platform(url):
    """
    Identify which platform a URL belongs to.
    """

    try:
        domain = urlparse(url).netloc.lower()

        # Remove www.
        domain = domain.replace("www.", "")

        for supported_domain, platform in SUPPORTED_PLATFORMS.items():

            if supported_domain in domain:
                return platform

        return "Other"

    except Exception:
        return "Unknown"


def discover_profiles(search_results):
    """
    Convert search results into potential profile candidates.
    """

    candidates = []

    for result in search_results:

        url = result.get("url", "")

        if not url:
            continue

        platform = identify_platform(url)

        candidate = {
            "platform": platform,
            "title": result.get("title", ""),
            "url": url,
            "snippet": result.get("snippet", "")
        }

        candidates.append(candidate)

    return candidates