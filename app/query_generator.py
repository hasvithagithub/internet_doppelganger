PLATFORMS = {
    "GitHub": "github.com",
    "LinkedIn": "linkedin.com",
    "Kaggle": "kaggle.com",
    "Medium": "medium.com",
    "Dev.to": "dev.to",
    "Pinterest": "pinterest.com"
}


def generate_username_variants(identity):
    """
    Generate a small number of likely username variants.
    """

    words = identity.lower().split()

    if not words:
        return []

    variants = []

    # All words together
    variants.append("".join(words))

    # First + last name
    if len(words) >= 2:
        variants.append(words[0] + words[-1])

    # Last + first name
    if len(words) >= 2:
        variants.append(words[-1] + words[0])

    # First initial + last name
    if len(words) >= 2:
        variants.append(words[0][0] + words[-1])

    # Remove duplicates
    return list(dict.fromkeys(variants))


def generate_queries(name, username=None, university=None):
    """
    Generate a small set of high-value search queries.
    """

    queries = []

    # ------------------------------------------------
    # 1. Exact full name
    # ------------------------------------------------

    queries.append(f'"{name}"')

    # ------------------------------------------------
    # 2. Platform-specific exact name searches
    # ------------------------------------------------

    for domain in PLATFORMS.values():

        queries.append(
            f'"{name}" site:{domain}'
        )

    # ------------------------------------------------
    # 3. Username search
    # ------------------------------------------------

    if username:

        queries.append(
            f'"{username}"'
        )

    else:

        # Only use the strongest username variant
        variants = generate_username_variants(name)

        if variants:

            queries.append(
                f'"{variants[0]}"'
            )

    # ------------------------------------------------
    # 4. University search
    # ------------------------------------------------

    if university:

        queries.append(
            f'"{name}" "{university}"'
        )

    # ------------------------------------------------
    # Remove duplicates
    # ------------------------------------------------

    return list(dict.fromkeys(queries))