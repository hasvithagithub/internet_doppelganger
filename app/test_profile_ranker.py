from profile_ranker import (
    rank_profiles,
    display_ranked_profiles
)


# ============================================================
# REFERENCE PERSON
# ============================================================

reference = {

    "name_mentions": [
        "hari",
        "hasvitha",
        "sai"
    ],

    "username": "harihasvitha",

    "organizations": [
        "Matrusri Engineering College"
    ],

    "platform": "Reference"
}


# ============================================================
# SAMPLE DISCOVERED PROFILES
# ============================================================

candidates = [

    {
        "title": "Hasvitha Sai Hari's Post",

        "url": "https://linkedin.com/example",

        "snippet": (
            "Hasvitha Sai Hari. "
            "Pursuing Computer Science Engineering "
            "@ Matrusri Engineering College"
        ),

        "platform": "LinkedIn",

        "username": "hasvitha-sai-hari",

        "name_mentions": [
            "hari",
            "hasvitha",
            "sai"
        ],

        "organizations": [
            "Matrusri Engineering College"
        ]
    },


    {
        "title": "Hari Hasvitha Sai",

        "url": "https://pinterest.com/example",

        "snippet": (
            "Hari Hasvitha Sai"
        ),

        "platform": "Pinterest",

        "username": "harihasvitha",

        "name_mentions": [
            "hari",
            "hasvitha",
            "sai"
        ],

        "organizations": []
    },


    {
        "title": "Random Hari Sai Profile",

        "url": "https://example.com/random",

        "snippet": (
            "Hari Sai technology enthusiast"
        ),

        "platform": "Other",

        "username": "harisai123",

        "name_mentions": [
            "hari",
            "sai"
        ],

        "organizations": []
    },

    {
        "title": "Only Name Match",
        "url": "https://example.com/name",
        "snippet": "Hari Hasvitha Sai is a person.",
        "platform": "Other",
        "name_mentions": ["hari", "hasvitha", "sai"],
        "organizations": []
    }
]


# ============================================================
# RUN RANKER
# ============================================================

ranked_profiles = rank_profiles(
    reference,
    candidates
)


# ============================================================
# DISPLAY
# ============================================================

display_ranked_profiles(
    ranked_profiles
)