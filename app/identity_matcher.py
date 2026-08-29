import re
from difflib import SequenceMatcher


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Convert text into a clean, comparable format.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Replace special characters with spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# STRING SIMILARITY
# ============================================================

def string_similarity(text1, text2):
    """
    Compare two strings.

    Returns:
        float between 0 and 1
    """

    text1 = normalize_text(text1)
    text2 = normalize_text(text2)

    if not text1 or not text2:
        return 0.0

    return round(
        SequenceMatcher(
            None,
            text1,
            text2
        ).ratio(),
        2
    )


# ============================================================
# NAME SIMILARITY
# ============================================================

def calculate_name_similarity(evidence1, evidence2):
    """
    Compare the name words found in two results.

    Example:

        ["hari", "hasvitha", "sai"]
        ["hari", "hasvitha", "sai"]

    gives a high similarity.
    """

    mentions1 = evidence1.get(
        "name_mentions",
        []
    )

    mentions2 = evidence2.get(
        "name_mentions",
        []
    )

    if not mentions1 or not mentions2:
        return 0.0

    set1 = {
        normalize_text(word)
        for word in mentions1
        if normalize_text(word)
    }

    set2 = {
        normalize_text(word)
        for word in mentions2
        if normalize_text(word)
    }

    if not set1 or not set2:
        return 0.0

    intersection = set1.intersection(set2)
    union = set1.union(set2)

    if not union:
        return 0.0

    return round(
        len(intersection) / len(union),
        2
    )


# ============================================================
# USERNAME SIMILARITY
# ============================================================

def calculate_username_similarity(
    evidence1,
    evidence2
):
    """
    Compare usernames from two profiles.
    """

    username1 = evidence1.get(
        "username"
    )

    username2 = evidence2.get(
        "username"
    )

    if not username1 or not username2:
        return 0.0

    return string_similarity(
        username1,
        username2
    )


# ============================================================
# ORGANIZATION SIMILARITY
# ============================================================

def calculate_organization_similarity(
    evidence1,
    evidence2
):
    """
    Compare colleges, universities,
    companies, or other organizations.
    """

    organizations1 = evidence1.get(
        "organizations",
        []
    )

    organizations2 = evidence2.get(
        "organizations",
        []
    )

    if not organizations1 or not organizations2:
        return 0.0

    best_score = 0.0

    for org1 in organizations1:

        for org2 in organizations2:

            score = string_similarity(
                org1,
                org2
            )

            best_score = max(
                best_score,
                score
            )

    return round(
        best_score,
        2
    )


# ============================================================
# PLATFORM SIGNAL
# ============================================================

def calculate_platform_signal(
    evidence1,
    evidence2
):
    """
    Platform is only a weak signal.

    Example:

        LinkedIn + LinkedIn = small positive signal

        LinkedIn + GitHub = no penalty

    Different platforms do NOT mean
    different people.
    """

    platform1 = evidence1.get(
        "platform"
    )

    platform2 = evidence2.get(
        "platform"
    )

    if not platform1 or not platform2:
        return 0.0

    if platform1.lower() == platform2.lower():
        return 1.0

    return 0.0


# ============================================================
# IDENTITY MATCH SCORE
# ============================================================

def calculate_match_score(
    evidence1,
    evidence2
):
    """
    Compare two pieces of web evidence
    and calculate how likely they are to
    belong to the same person.

    Missing evidence is ignored instead
    of being treated as negative evidence.
    """

    # --------------------------------------------------------
    # Calculate individual signals
    # --------------------------------------------------------

    name_score = calculate_name_similarity(
        evidence1,
        evidence2
    )

    username_score = calculate_username_similarity(
        evidence1,
        evidence2
    )

    organization_score = calculate_organization_similarity(
        evidence1,
        evidence2
    )

    platform_score = calculate_platform_signal(
        evidence1,
        evidence2
    )


    # --------------------------------------------------------
    # Available evidence
    # --------------------------------------------------------

    signals = []


    # Name
    if (
        evidence1.get("name_mentions")
        and evidence2.get("name_mentions")
    ):

        signals.append(
            (
                "name",
                name_score,
                0.45
            )
        )


    # Username
    if (
        evidence1.get("username")
        and evidence2.get("username")
    ):

        signals.append(
            (
                "username",
                username_score,
                0.35
            )
        )


    # Organization
    if (
        evidence1.get("organizations")
        and evidence2.get("organizations")
    ):

        signals.append(
            (
                "organization",
                organization_score,
                0.15
            )
        )


    # Platform
    if (
        evidence1.get("platform")
        and evidence2.get("platform")
        and
        evidence1.get("platform").lower()
        ==
        evidence2.get("platform").lower()
    ):

        signals.append(
            (
                "platform",
                platform_score,
                0.05
            )
        )


    # --------------------------------------------------------
    # No usable evidence
    # --------------------------------------------------------

    if not signals:

        return {
            "score": 0.0,

            "confidence": "Insufficient Evidence",

            "signals": {
                "name_similarity": name_score,
                "username_similarity": username_score,
                "organization_similarity": organization_score,
                "platform_signal": platform_score
            }
        }


    # --------------------------------------------------------
    # Normalize weights
    # --------------------------------------------------------

    total_weight = sum(
        weight
        for _, _, weight in signals
    )

    weighted_score = sum(
        score * weight
        for _, score, weight in signals
    )

    normalized_score = (
        weighted_score / total_weight
    )


    final_score = round(
        normalized_score * 100,
        2
    )


    # --------------------------------------------------------
    # Confidence classification
    # --------------------------------------------------------

    if final_score >= 80:

        confidence = "High"

    elif final_score >= 55:

        confidence = "Medium"

    else:

        confidence = "Low"


    # --------------------------------------------------------
    # Return complete result
    # --------------------------------------------------------

    return {

        "score": final_score,

        "confidence": confidence,

        "signals": {

            "name_similarity": name_score,

            "username_similarity": username_score,

            "organization_similarity": organization_score,

            "platform_signal": platform_score

        }
    }