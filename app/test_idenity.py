from identity_matcher import calculate_match_score


linkedin_evidence = {

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
}


pinterest_evidence = {

    "platform": "Pinterest",

    "username": "harihasvitha",

    "name_mentions": [
        "hari",
        "hasvitha",
        "sai"
    ],

    "organizations": []
}


result = calculate_match_score(
    linkedin_evidence,
    pinterest_evidence
)


print("\nIdentity Match Result")
print("=" * 40)

print(
    f"Score: {result['score']}%"
)

print(
    f"Confidence: {result['confidence']}"
)

print("\nSignals:")

for signal, value in result["signals"].items():

    print(
        f"{signal}: {value}"
    )