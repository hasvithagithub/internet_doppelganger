from search import search_web
from query_generator import generate_queries
from evidence_extractor import extract_evidence
from profile_filter import (
    filter_profiles,
    display_filter_summary
)
from profile_ranker import (
    rank_profiles,
    display_ranked_profiles
)


def main():

    print("=" * 70)
    print("              INTERNET DOPPELGÄNGER")
    print("              Profile Discovery Engine")
    print("=" * 70)

    # ============================================================
    # 1. COLLECT REFERENCE IDENTITY
    # ============================================================

    full_name = input(
        "\nEnter full name: "
    ).strip()

    if not full_name:

        print("Full name is required.")

        return

    username = input(
        "Enter username (optional): "
    ).strip()

    university = input(
        "Enter university/college (optional): "
    ).strip()

    # ============================================================
    # 2. CREATE REFERENCE PROFILE
    # ============================================================

    reference_evidence = {

        "name_mentions": full_name.lower().split(),

        "username": (
            username
            if username
            else None
        ),

        "organizations": (
            [university]
            if university
            else []
        ),

        "platform": "Reference"
    }

    # ============================================================
    # 3. GENERATE TARGETED SEARCH QUERIES
    # ============================================================

    print("\nGenerating targeted searches...")

    queries = generate_queries(
        full_name,
        username=username,
        university=university
    )

    print(
        f"Generated {len(queries)} search queries.\n"
    )

    # ============================================================
    # 4. SEARCH THE WEB
    # ============================================================

    all_results = []

    for query in queries:

        print(
            f'Searching: "{query}"'
        )

        results = search_web(query)

        if results:

            all_results.extend(
                results
            )

    # ============================================================
    # 5. REMOVE DUPLICATE URLS
    # ============================================================

    unique_results = {}

    for result in all_results:

        url = result.get(
            "url"
        )

        if url:

            unique_results[url] = result

    unique_results = list(
        unique_results.values()
    )

    print("\n" + "=" * 70)

    print(
        f"Total unique search results: "
        f"{len(unique_results)}"
    )

    print("=" * 70)

    if not unique_results:

        print(
            "\nNo search results found."
        )

        return

    # ============================================================
    # 6. EXTRACT IDENTITY EVIDENCE
    # ============================================================

    print(
        "\nExtracting identity evidence...\n"
    )

    extracted_profiles = []

    for index, result in enumerate(
        unique_results,
        start=1
    ):

        print(
            f"Processing result "
            f"{index}/{len(unique_results)}"
        )

        try:

            evidence = extract_evidence(
                result,
                full_name
            )

            # ----------------------------------------------------
            # Preserve original search information
            # ----------------------------------------------------

            evidence["title"] = result.get(
                "title",
                ""
            )

            evidence["url"] = result.get(
                "url",
                ""
            )

            evidence["snippet"] = result.get(
                "snippet",
                ""
            )

            extracted_profiles.append(
                evidence
            )

        except Exception as error:

            print(
                f"Evidence extraction failed: "
                f"{error}"
            )

    # ============================================================
    # 7. CHECK EXTRACTED EVIDENCE
    # ============================================================

    print("\n" + "=" * 70)

    print(
        f"Profiles with extracted evidence: "
        f"{len(extracted_profiles)}"
    )

    print("=" * 70)

    if not extracted_profiles:

        print(
            "\nNo identity evidence could be extracted."
        )

        return

    # ============================================================
    # 8. FILTER NON-PROFILE RESULTS
    # ============================================================

    filtered_profiles = filter_profiles(
        extracted_profiles,
        minimum_name_score=0.5
    )

    display_filter_summary(
        len(extracted_profiles),
        filtered_profiles
    )

    if not filtered_profiles:

        print(
            "\nNo potential profile pages found."
        )

        return

    # ============================================================
    # 9. RANK POTENTIAL PROFILES
    # ============================================================

    print(
        "\nRanking potential profiles..."
    )

    ranked_profiles = rank_profiles(
        reference_evidence,
        filtered_profiles
    )

    # ============================================================
    # 10. DISPLAY TOP PROFILES
    # ============================================================

    display_ranked_profiles(
        ranked_profiles,
        top_n=10
    )


# ================================================================
# PROGRAM ENTRY POINT
# ================================================================

if __name__ == "__main__":

    main()