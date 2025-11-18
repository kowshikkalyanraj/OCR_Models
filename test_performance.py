#!/usr/bin/env python3
"""
Performance test script for OCR Label Extractor.
Optimized for persistent sessions and <2s inference.
"""

import time
import re
import json
import ollama
from ai_extractor import OLLAMA_MODEL


def warm_up_model():
    """Pre-warm the model once before tests."""
    print("🔥 Pre-warming the model...")
    try:
        _ = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": "warmup"}],
        )
        print("✅ Model warmed up and ready!\n")
    except Exception as e:
        print(f"⚠️ Warm-up failed: {e}")


def test_extraction_performance():
    """Run speed + accuracy tests."""
    test_cases = [
        "lex2 2.8 lbs, 2821 carradale dr, 95661-4047 roseville, ca, fat1, united states, zoey dong, dsm1, 0503 dsm1, tba132376390000, cycle 1, a sm1",
        "batavia stkllt, special instructiu, metr 4684 3913 8542, g, ca 8206s, 95661, o, 230, 2, paper, fedex, mps 46843913 8553, frun, 2164 n, 9622 00 19 0 000 000 0000 0 00 4684 3913 8553, 8150 sierra college blvd ste, syta saephan, notifil, roseville ca 95661, ground, of 2, 214 787-430o, us, bill sender",
        "ship to, ups ground, 41 lbs, tracking : 1z v4w 195 03 6500 6276, manautr, 2821 carradale dr, ree v0084700946203420100402, etxk-0806:, 0f 1, 1, ky dong, 95661-4047, ref, wi 34.18, 17, nippina, 310 99-085, ca 956 0-01, billing pip, roseville ca, cwtainity"
    ]

    print("🚀 Performance Test - OCR Label Extractor\n")
    print(f"Model: {OLLAMA_MODEL}")
    print(f"Target: <2 seconds per extraction\n")
    print("=" * 60)

    # ✅ Warm up first
    warm_up_model()

    # ✅ Persistent client for all calls
    client = ollama.Client(host="http://localhost:11434")

    times = []
    for i, text in enumerate(test_cases, 1):
        print(f"\n📋 Test Case {i}:")
        print(f"Text: {text[:80]}...")

        start = time.time()
        response = client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": f"Extract recipient name and address as JSON:\n{text}"
                }
            ],
        )
        elapsed = time.time() - start
        times.append(elapsed)

        content = response["message"]["content"]
        match = re.search(r"\{.*?\}", content, re.DOTALL)
        if match:
            try:
                result = json.loads(match.group(0))
            except json.JSONDecodeError:
                result = {}
        else:
            result = {}

        if result:
            print(f"✅ Name: {result.get('recipient_name')}")
            print(f"✅ Address: {result.get('address')}")
        else:
            print("❌ Extraction failed")

        status = "✅" if elapsed < 2.0 else "⚠️"
        print(f"{status} Time: {elapsed:.2f}s")

    print("\n" + "=" * 60)
    print("📊 Performance Summary:")
    print(f"  Average time: {sum(times)/len(times):.2f}s")
    print(f"  Min time: {min(times):.2f}s")
    print(f"  Max time: {max(times):.2f}s")
    print(f"  Target met: {sum(1 for t in times if t < 2.0)}/{len(times)} tests")

    if all(t < 2.0 for t in times):
        print("\n✅ All tests completed under 2 seconds!")
    else:
        print("\n⚠️  Some tests exceeded 2 seconds. Recommendations:")
        print("  - Ensure OLLAMA_KEEP_ALIVE=5m is active")
        print("  - GPU acceleration enabled (ollama ps)")
        print("  - Model: llama3.2:1b (already optimal)")


if __name__ == "__main__":
    test_extraction_performance()
