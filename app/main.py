from search import search_web
from query_generator import generate_queries


def main():

    print("=" * 60)
    print("              INTERNET DOPPELGÄNGER")
    print("              Web Discovery Engine")
    print("=" * 60)

    # ---------------------------------------------
    # Get single user input
    # ---------------------------------------------

    identity = input(
        "\nEnter a name or username: "
    ).strip()

    if not identity:
        print("Please enter a name or username.")
        return

    print(f"\nSearching the web for: {identity}")
    print("Generating targeted searches...\n")

    # ---------------------------------------------
    # Generate optimized queries
    # ---------------------------------------------

    queries = generate_queries(identity)

    print(f"Generated {len(queries)} search queries.\n")

    # ---------------------------------------------
    # Search
    # ---------------------------------------------

    all_results = []

    for query in queries:

        print(f"Searching: {query}")

        results = search_web(query)

        if results:
            all_results.extend(results)

    # ---------------------------------------------
    # Remove duplicate URLs
    # ---------------------------------------------

    unique_results = {}

    for result in all_results:

        url = result.get("url")

        if url:
            unique_results[url] = result

    results = list(unique_results.values())

    # ---------------------------------------------
    # Display results
    # ---------------------------------------------

    print("\n" + "=" * 60)
    print(f"Total unique results: {len(results)}")
    print("=" * 60)

    if not results:
        print("\nNo results found.")
        return

    for index, result in enumerate(results, start=1):

        print(f"\n{index}. {result.get('title', 'No title')}")
        print(f"   URL: {result.get('url', 'No URL')}")

        snippet = result.get("snippet")

        if snippet:
            print(f"   Snippet: {snippet}")

        print("-" * 60)


if __name__ == "__main__":
    main()