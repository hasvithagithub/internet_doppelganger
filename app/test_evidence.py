from evidence_extractor import extract_evidence


test_result = {
    "title": "Hasvitha Sai Hari's Post",
    "url": "https://www.linkedin.com/posts/hasvitha-sai-hari-96b6232a7_ai-hackathon-automation-activity-7435006008776699904-dPDx",
    "snippet": "Hasvitha Sai Hari. Pursuing Computer Science Engineering @ Matrusri Engineering College"
}


evidence = extract_evidence(
    test_result,
    "Hari Hasvitha Sai"
)


print("\nExtracted Evidence:\n")

for key, value in evidence.items():

    print(f"{key}: {value}")