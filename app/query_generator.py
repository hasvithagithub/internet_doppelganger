# ============================================================
# QUERY GENERATOR
# ============================================================

PLATFORMS = {
    "GitHub": "github.com",
    "LinkedIn": "linkedin.com",
    "Kaggle": "kaggle.com",
    "Medium": "medium.com",
    "Dev.to": "dev.to",
    "Pinterest": "pinterest.com"
}


# ============================================================
# USERNAME VARIANTS
# ============================================================

def generate_username_variants(identity):
    """
    Generate likely username variations from a person's name.
    """

    words = identity.lower().split()

    if not words:
        return []

    variants = []

    # Remove spaces
    variants.append(
        "".join(words)
    )

    # Add separated variants
    variants.append(
        ".".join(words)
    )
    variants.append(
        "_".join(words)
    )

    # First + last
    if len(words) >= 2:

        variants.append(
            words[0] + words[-1]
        )
        variants.append(
            words[0] + "." + words[-1]
        )
        variants.append(
            words[0] + "_" + words[-1]
        )

    # Last + first
    if len(words) >= 2:

        variants.append(
            words[-1] + words[0]
        )
        variants.append(
            words[-1] + "." + words[0]
        )
        variants.append(
            words[-1] + "_" + words[0]
        )

    # First initial + last
    if len(words) >= 2:

        variants.append(
            words[0][0] + words[-1]
        )
        variants.append(
            words[0][0] + "." + words[-1]
        )
        variants.append(
            words[0][0] + "_" + words[-1]
        )

    # First + middle + last initials
    if len(words) >= 3:

        variants.append(
            words[0][0]
            + words[1][0]
            + words[-1]
        )

    # First initial + middle + last
    if len(words) >= 3:

        variants.append(
            words[0][0]
            + words[1]
            + words[-1]
        )

    # Remove duplicates
    return list(
        dict.fromkeys(variants)
    )


# ============================================================
# GENERATE QUERIES
# ============================================================

def generate_queries(
    name,
    username=None,
    university=None
):
    """
    Generate targeted web-search queries for
    discovering potential online profiles.
    """

    queries = []

    # --------------------------------------------------------
    # 1. Exact full name
    # --------------------------------------------------------

    queries.append(
        f'"{name}"'
    )

    # --------------------------------------------------------
    # 2. Platform-specific name searches
    # --------------------------------------------------------

    for domain in PLATFORMS.values():

        # Exact phrase
        queries.append(
            f'"{name}" site:{domain}'
        )

        # Broad search (handles different name ordering)
        queries.append(
            f'{name} site:{domain}'
        )

    # --------------------------------------------------------
    # 3. Username searches
    # --------------------------------------------------------

    if username:

        # Exact supplied username
        queries.append(
            f'"{username}"'
        )

        # Search username on each platform
        for domain in PLATFORMS.values():

            queries.append(
                f'"{username}" site:{domain}'
            )

    else:

        # Generate username variants
        variants = generate_username_variants(
            name
        )

        # Search each variant
        for variant in variants:

            queries.append(
                f'"{variant}"'
            )

    # --------------------------------------------------------
    # 4. Name + university
    # --------------------------------------------------------

    if university:

        queries.append(
            f'"{name}" "{university}"'
        )

        # Search university + platform
        for domain in PLATFORMS.values():

            queries.append(
                f'"{name}" "{university}" site:{domain}'
            )
            queries.append(
                f'{name} "{university}" site:{domain}'
            )

    # --------------------------------------------------------
    # 5. Developer-oriented searches
    # --------------------------------------------------------

    queries.append(
        f'"{name}" developer'
    )

    queries.append(
        f'"{name}" engineer'
    )

    queries.append(
        f'"{name}" student'
    )

    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    queries = list(
        dict.fromkeys(queries)
    )

    return queries