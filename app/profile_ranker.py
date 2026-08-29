from identity_matcher import calculate_match_score


# ============================================================
# PROFILE RANKER
# ============================================================

def rank_profiles(reference_evidence, candidates):
    """
    Compare every candidate profile against the
    reference identity and rank them by confidence.

    Args:
        reference_evidence (dict):
            Evidence representing the person we are searching for.

        candidates (list):
            List of extracted evidence dictionaries.

    Returns:
        list:
            Candidates sorted from highest score to lowest score.
    """

    ranked_profiles = []

    for candidate in candidates:

        # ----------------------------------------------------
        # Calculate identity match
        # ----------------------------------------------------

        match_result = calculate_match_score(
            reference_evidence,
            candidate
        )

        # ----------------------------------------------------
        # Combine candidate + score
        # ----------------------------------------------------

        ranked_profile = {
            "title": candidate.get(
                "title",
                "No title"
            ),

            "url": candidate.get(
                "url",
                ""
            ),

            "snippet": candidate.get(
                "snippet",
                ""
            ),

            "platform": candidate.get(
                "platform",
                "Unknown"
            ),

            "username": candidate.get(
                "username"
            ),

            "organizations": candidate.get(
                "organizations",
                []
            ),

            "score": match_result.get(
                "score",
                0
            ),

            "confidence": match_result.get(
                "confidence",
                "Unknown"
            ),

            "signals": match_result.get(
                "signals",
                {}
            )
        }

        ranked_profiles.append(
            ranked_profile
        )


    # --------------------------------------------------------
    # Sort by confidence then score
    # --------------------------------------------------------

    confidence_levels = {
        "High": 3,
        "Medium": 2,
        "Low": 1,
        "Unknown": 0,
        "Insufficient Evidence": -1
    }

    ranked_profiles.sort(
        key=lambda profile: (
            confidence_levels.get(profile.get("confidence", "Unknown"), 0),
            profile["score"]
        ),
        reverse=True
    )


    return ranked_profiles


# ============================================================
# DISPLAY RANKED PROFILES
# ============================================================

def display_ranked_profiles(
    ranked_profiles,
    top_n=10
):
    """
    Display the highest-ranked profiles.
    """

    print("\n")
    print("=" * 70)
    print("              TOP POTENTIAL PROFILES")
    print("=" * 70)


    if not ranked_profiles:

        print("\nNo profiles available.")

        return


    # --------------------------------------------------------
    # Display top profiles
    # --------------------------------------------------------

    for index, profile in enumerate(
        ranked_profiles[:top_n],
        start=1
    ):

        print(
            f"\n{index}. "
            f"{profile.get('platform', 'Unknown')}"
        )

        print(
            f"   Score: "
            f"{profile.get('score', 0)}%"
        )

        print(
            f"   Confidence: "
            f"{profile.get('confidence', 'Unknown')}"
        )

        print(
            f"   Title: "
            f"{profile.get('title', 'No title')}"
        )

        print(
            f"   URL: "
            f"{profile.get('url', 'No URL')}"
        )

        username = profile.get(
            "username"
        )

        if username:

            print(
                f"   Username: {username}"
            )


        organizations = profile.get(
            "organizations",
            []
        )

        if organizations:

            print(
                f"   Organizations: "
                f"{', '.join(organizations)}"
            )


        # ----------------------------------------------------
        # Evidence signals
        # ----------------------------------------------------

        signals = profile.get(
            "signals",
            {}
        )

        if signals:

            print("   Evidence:")

            print(
                f"      Name similarity: "
                f"{signals.get('name_similarity', 0)}"
            )

            print(
                f"      Username similarity: "
                f"{signals.get('username_similarity', 0)}"
            )

            print(
                f"      Organization similarity: "
                f"{signals.get('organization_similarity', 0)}"
            )

        print("-" * 70)