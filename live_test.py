"""
Optional live validation.

Run:
    python live_test.py

This checks 10 articles across different fact types against the live
English Wikipedia API. Internet access is required.
"""
from app import compare_fact

CASES = [
    ("Narendra Modi", "Birth Date"),
    ("Google", "Founder"),
    ("Apple Inc.", "Founder"),
    ("Microsoft", "Founder"),
    ("Amazon (company)", "Founder"),
    ("Tesla, Inc.", "Location"),
    ("Meta Platforms", "Location"),
    ("Japan", "Country"),
    ("India", "Country"),
    ("Albert Einstein", "Birth Date"),
]

for title, fact_type in CASES:
    try:
        result = compare_fact(title, fact_type)
        print(f"{title:25} | {fact_type:12} | {result['status']}")
        if result["evidence"]:
            print("  Evidence:", result["evidence"])
    except Exception as exc:
        print(f"{title:25} | ERROR | {exc}")
