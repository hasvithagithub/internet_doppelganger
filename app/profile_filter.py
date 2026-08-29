from urllib.parse import urlparse


# ============================================================
# SUPPORTED PROFILE URL PATTERNS
# ============================================================

def is_profile_url(url):
    """
    Determine whether a URL is likely to represent
    an actual user profile rather than an article,
    post, document, search page, etc.
    """

    if not url:
        return False

    try:
        parsed = urlparse(url)

        domain = parsed.netloc.lower().replace("www.", "")
        path = parsed.path.strip("/")

        parts = [
            part for part in path.split("/")
            if part
        ]

        # ----------------------------------------------------
        # LinkedIn
        # ----------------------------------------------------

        if domain.endswith("linkedin.com"):

            # Valid profile:
            # linkedin.com/in/username

            if len(parts) >= 2 and parts[0].lower() == "in":
                return True

            # Posts, jobs, company pages, etc.
            return False


        # ----------------------------------------------------
        # GitHub
        # ----------------------------------------------------

        if domain == "github.com":

            if not parts:
                return False

            reserved = {
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
                "pulls",
                "about",
                "pricing"
            }

            # github.com/username
            if len(parts) == 1 and parts[0].lower() not in reserved:
                return True

            return False


        # ----------------------------------------------------
        # Kaggle
        # ----------------------------------------------------

        if domain == "kaggle.com":

            if not parts:
                return False

            reserved = {
                "competitions",
                "datasets",
                "code",
                "models",
                "discussions",
                "learn",
                "search"
            }

            # kaggle.com/username
            if len(parts) == 1 and parts[0].lower() not in reserved:
                return True

            return False


        # ----------------------------------------------------
        # Medium
        # ----------------------------------------------------

        if domain == "medium.com":

            if not parts:
                return False

            # medium.com/@username
            if parts[0].startswith("@"):
                return True

            reserved = {
                "tag",
                "topic",
                "about",
                "search",
                "membership",
                "plans"
            }

            if len(parts) == 1 and parts[0].lower() not in reserved:
                return True

            return False


        # ----------------------------------------------------
        # Dev.to
        # ----------------------------------------------------

        if domain == "dev.to":

            if not parts:
                return False

            reserved = {
                "search",
                "tags",
                "top",
                "latest",
                "readinglist",
                "pod",
                "videos"
            }

            if len(parts) == 1 and parts[0].lower() not in reserved:
                return True

            return False


        # ----------------------------------------------------
        # Pinterest
        # ----------------------------------------------------

        if domain.endswith("pinterest.com"):

            if not parts:
                return False

            reserved = {
                "pin",
                "ideas",
                "search",
                "topics",
                "settings",
                "business"
            }

            # pinterest.com/username
            if len(parts) == 1 and parts[0].lower() not in reserved:
                return True

            return False


    except Exception:
        return False


    return False


# ============================================================
# NAME VALIDATION
# ============================================================

def has_strong_name_match(profile, minimum_score=0.5):
    """
    Check whether the candidate contains enough
    of the target person's name.

    A profile with no meaningful name match
    should not survive the identity filter.
    """

    score = profile.get(
        "name_match_score",
        0.0
    )

    return score >= minimum_score


# ============================================================
# USERNAME VALIDATION
# ============================================================

def has_username(profile):
    """
    Check whether the profile has a detected username.
    """

    username = profile.get(
        "username"
    )

    return bool(username)


# ============================================================
# FILTER SINGLE PROFILE
# ============================================================

def is_valid_profile(
    profile,
    minimum_name_score=0.5
):
    """
    Decide whether a search result should remain
    in the candidate profile list.

    Rules:

    1. URL must look like a real profile.
    2. Candidate must have a meaningful name match.
    """

    url = profile.get(
        "url",
        ""
    )

    # --------------------------------------------------------
    # Rule 1: Must be a profile URL
    # --------------------------------------------------------

    if not is_profile_url(url):
        return False


    # --------------------------------------------------------
    # Rule 2: Must have meaningful name evidence
    # --------------------------------------------------------

    if not has_strong_name_match(
        profile,
        minimum_name_score
    ):
        return False


    return True


# ============================================================
# FILTER ALL PROFILES
# ============================================================

def filter_profiles(
    profiles,
    minimum_name_score=0.5
):
    """
    Filter a collection of extracted profiles.

    Returns:
        list of likely genuine profile candidates.
    """

    filtered_profiles = []

    for profile in profiles:

        if is_valid_profile(
            profile,
            minimum_name_score
        ):

            filtered_profiles.append(
                profile
            )

    return filtered_profiles


# ============================================================
# DISPLAY FILTER RESULTS
# ============================================================

def display_filter_summary(
    original_count,
    filtered_profiles
):
    """
    Display a simple filtering summary.
    """

    print(
        "\nFiltering non-profile search results..."
    )

    print(
        f"Search results before filtering: "
        f"{original_count}"
    )

    print(
        f"Potential profile pages remaining: "
        f"{len(filtered_profiles)}"
    )
    