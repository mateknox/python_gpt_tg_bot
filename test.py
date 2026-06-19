from sources import MediaSearchEngine

if __name__ == '__main__':
    print("Executing structural tests...")
    test_engine = MediaSearchEngine()

    # Test Gemini
    print("\n[Test 1] Testing Gemini Connectivity...")
    print(test_engine.ask_gemini("Say hello!"))

    # Test Genre API
    print("\n[Test 2] Testing OMDb Query Pipelines...")
    items = test_engine.search_movies_by_genre("comedy")
    print(f"Retrieved {len(items)} raw list records.")

    if items:
        first_id = [s for s in items[0].split("/") if s][-1]
        print(f"Extracted key: {first_id}")
        print(f"Details Payload: {test_engine.get_movie_details(first_id)}")
