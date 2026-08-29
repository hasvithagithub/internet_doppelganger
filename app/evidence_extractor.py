import re
from urllib.parse import urlparse


# -------------------------------------------------
# Supported platforms
# -------------------------------------------------

PLATFORMS = {
    "github.com": "GitHub",
    "linkedin.com": "LinkedIn",
    "kaggle.com": "Kaggle",
    "medium.com": "Medium",
    "dev.to": "Dev.to",
    "pinterest.com": "Pinterest"
}


# -------------------------------------------------
# Detect platform
# -------------------------------------------------

def detect_platform(url):
    """
    Identify the platform from a URL.
    """

    if not url:
        return "Other"

    try:
        domain = urlparse(url).netloc.lower()
        domain = domain.replace("www.", "")

        for platform_domain, platform_name in PLATFORMS.items():

            if (
                domain == platform_domain
                or domain.endswith("." + platform_domain)
            ):
                return platform_name

    except Exception:
        pass

    return "Other"


# -------------------------------------------------
# Extract URL path parts
# -------------------------------------------------

def extract_url_parts(url):
    """
    Extract useful parts from a URL path.
    """

    if not url:
        return []

    try:
        parsed = urlparse(url)

        path = parsed.path.strip("/")

        parts = [
            part for part in path.split("/")
            if part
        ]

        return parts

    except Exception:
        return []


# -------------------------------------------------
# Extract username
# -------------------------------------------------

def extract_username(url):
    """
    Try to identify a username from common
    platform URL patterns.
    """

    platform = detect_platform(url)
    parts = extract_url_parts(url)

    if not parts:
        return None


    # ---------------------------------------------
    # GitHub
    # ---------------------------------------------

    if platform == "GitHub":

        reserved_paths = [
            "features",
            "topics",
            "collections",
            "marketplace",
            "explore",
            "orgs",
            "login",
            "signup",
            "settings",
            "search",
            "notifications",
            "issues",
            "pulls"
        ]

        if parts[0].lower() not in reserved_paths:
            return parts[0]


    # ---------------------------------------------
    # LinkedIn
    # ---------------------------------------------

    if platform == "LinkedIn":

        # Actual profile:
        # linkedin.com/in/username

        if parts[0].lower() == "in" and len(parts) >= 2:
            return parts[1]

        # Posts are not treated as profiles.
        if parts[0].lower() == "posts":
            return None


    # ---------------------------------------------
    # Kaggle
    # ---------------------------------------------

    if platform == "Kaggle":

        if parts[0].lower() in [
            "code",
            "datasets",
            "models"
        ]:

            if len(parts) >= 2:
                return parts[1]

        reserved_paths = [
            "competitions",
            "datasets",
            "code",
            "models",
            "discussions",
            "learn",
            "search"
        ]

        if parts[0].lower() not in reserved_paths:
            return parts[0]


    # ---------------------------------------------
    # Medium
    # ---------------------------------------------

    if platform == "Medium":

        if parts[0].startswith("@"):
            return parts[0][1:]

        reserved_paths = [
            "tag",
            "topic",
            "about",
            "search",
            "membership",
            "plans"
        ]

        if parts[0].lower() not in reserved_paths:
            return parts[0]


    # ---------------------------------------------
    # Dev.to
    # ---------------------------------------------

    if platform == "Dev.to":

        reserved_paths = [
            "search",
            "tags",
            "top",
            "latest",
            "readinglist",
            "pod",
            "videos"
        ]

        if parts[0].lower() not in reserved_paths:
            return parts[0]


    # ---------------------------------------------
    # Pinterest
    # ---------------------------------------------

    if platform == "Pinterest":

        reserved_paths = [
            "pin",
            "ideas",
            "search",
            "topics",
            "settings",
            "business"
        ]

        if parts[0].lower() not in reserved_paths:
            return parts[0]


    return None


# -------------------------------------------------
# Extract name mentions
# -------------------------------------------------

def extract_name_mentions(text, target_name):
    """
    Find individual words from the target name
    that appear in the result text.
    """

    if not text or not target_name:
        return []

    text_lower = text.lower()

    name_words = re.findall(
        r"[a-zA-Z0-9]+",
        target_name.lower()
    )

    matches = []

    for word in name_words:

        pattern = r"\b" + re.escape(word) + r"\b"

        # Also allow matching just the initial if the word is > 1 char
        initial = word[0]
        initial_pattern = r"\b" + re.escape(initial) + r"\b"

        if re.search(pattern, text_lower) or (len(word) > 1 and re.search(initial_pattern, text_lower)):

            if word not in matches:
                matches.append(word)

    return matches


# -------------------------------------------------
# Calculate name match score
# -------------------------------------------------

def calculate_name_match_score(
    name_mentions,
    target_name
):
    """
    Calculate how much of the target name
    appears in the result.
    """

    if not target_name:
        return 0.0

    target_words = set(
        word.lower()
        for word in re.findall(
            r"[a-zA-Z0-9]+",
            target_name
        )
    )

    if not target_words:
        return 0.0

    matched_words = set(
        word.lower()
        for word in name_mentions
    )

    matched = target_words.intersection(
        matched_words
    )

    return round(
        len(matched) / len(target_words),
        2
    )


# -------------------------------------------------
# Extract organizations
# -------------------------------------------------

def extract_organizations(text):
    """
    Try to identify organizations, colleges,
    universities, and companies from text.
    """

    if not text:
        return []

    organizations = []


    # ---------------------------------------------
    # College / University patterns
    # ---------------------------------------------

    education_patterns = [

        r"(?:at|@|from|studying at|student at|pursuing.*?at)\s+"
        r"([A-Z][A-Za-z0-9&.,' -]{2,100}"
        r"(?:College|University|Institute|School)"
        r"(?:\s+of\s+[A-Za-z]+)?)",

        r"([A-Z][A-Za-z0-9&.,' -]{2,100}"
        r"(?:College|University|Institute|School))"
    ]


    for pattern in education_patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            organization = match.strip(
                " ,.-"
            )

            if organization:
                organizations.append(
                    organization
                )


    # ---------------------------------------------
    # Company / Organization patterns
    # ---------------------------------------------

    company_patterns = [

        r"(?:works at|working at|employee at|"
        r"employed at|intern at|interned at)\s+"
        r"([A-Z][A-Za-z0-9&.,' -]{2,100})",

        r"(?:@)\s+"
        r"([A-Z][A-Za-z0-9&.,' -]{2,100}"
        r"(?:Technologies|Technology|Solutions|"
        r"Systems|Labs|Limited|Ltd|Inc|Corp|"
        r"Company|Foundation))"
    ]


    for pattern in company_patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            organization = match.strip(
                " ,.-"
            )

            if organization:
                organizations.append(
                    organization
                )


    # ---------------------------------------------
    # Clean duplicates
    # ---------------------------------------------

    cleaned = []

    for organization in organizations:

        organization = re.sub(
            r"\s+",
            " ",
            organization
        ).strip()

        if (
            organization
            and organization.lower()
            not in [
                item.lower()
                for item in cleaned
            ]
        ):
            cleaned.append(
                organization
            )


    return cleaned


# -------------------------------------------------
# Extract all evidence from one result
# -------------------------------------------------

def extract_evidence(result, target_name):
    """
    Convert a raw search result into structured
    identity evidence.
    """

    title = result.get(
        "title",
        ""
    ).strip()

    url = result.get(
        "url",
        ""
    ).strip()

    snippet = result.get(
        "snippet",
        ""
    ).strip()


    # Combine title + snippet
    combined_text = (
        f"{title} {snippet}"
    )


    # Detect platform
    platform = detect_platform(
        url
    )


    # Extract username
    username = extract_username(
        url
    )


    # Extract name mentions
    name_mentions = extract_name_mentions(
        combined_text,
        target_name
    )


    # Calculate name match
    name_match_score = calculate_name_match_score(
        name_mentions,
        target_name
    )


    # Extract organizations
    organizations = extract_organizations(
        combined_text
    )


    return {
        "title": title,
        "url": url,
        "snippet": snippet,
        "platform": platform,
        "username": username,
        "name_mentions": name_mentions,
        "name_match_score": name_match_score,
        "organizations": organizations
    }


# -------------------------------------------------
# Extract evidence from multiple results
# -------------------------------------------------

def extract_all_evidence(results, target_name):
    """
    Extract structured evidence from all
    search results.
    """

    evidence = []

    for result in results:

        extracted = extract_evidence(
            result,
            target_name
        )

        evidence.append(
            extracted
        )

    return evidence