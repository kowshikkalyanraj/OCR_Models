#!/usr/bin/env python3
"""
Optimization script to ensure consistent <2 second performance.
This script:
1. Pre-loads the model into memory
2. Makes test calls to warm up the model
3. Monitors performance
4. Provides recommendations
"""

import time
import ollama
from ai_extractor import OLLAMA_MODEL, extract_with_ai


def warmup_model(model_name, num_warmup_calls=3):
    """Warm up the model with multiple calls."""
    print(f"🔥 Warming up model: {model_name}")
    print(f"⏳ Making {num_warmup_calls} warmup calls...")

    warmup_texts = [
        "test, 123 main st, new york, ny 10001, john doe",
        "sample, 456 oak ave, los angeles, ca 90001, jane smith",
        "example, 789 pine rd, chicago, il 60601, bob johnson",
    ]

    times = []
    for i, text in enumerate(warmup_texts[:num_warmup_calls], 1):
        start = time.time()
        try:
            response = ollama.chat(
                model=model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "Extract recipient name and address from OCR. Return JSON only.",
                    },
                    {"role": "user", "content": f"Extract from: {text}"},
                ],
                options={
                    "num_predict": 100,
                    "temperature": 0.1,
                },
            )
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"  Warmup {i}/{num_warmup_calls}: {elapsed:.2f}s")
        except Exception as e:
            print(f"  ⚠️ Warmup {i} failed: {e}")

    if times:
        avg_time = sum(times) / len(times)
        print(f"✅ Warmup complete. Average time: {avg_time:.2f}s")
        return avg_time
    return None


def test_performance(model_name, test_cases=5):
    """Test performance with actual extraction calls."""
    print(f"\n📊 Testing performance with {test_cases} extraction calls...")

    test_texts = [
        "lex2 2.8 lbs, 2821 carradale dr, 95661-4047 roseville, ca, fat1, united states, zoey dong, dsm1, 0503 dsm1, tba132376390000, cycle 1, a sm1",
        "batavia stkllt, special instructiu, metr 4684 3913 8542, g, ca 8206s, 95661, o, 230, 2, paper, fedex, mps 46843913 8553, frun, 2164 n, 9622 00 19 0 000 000 0000 0 00 4684 3913 8553, 8150 sierra college blvd ste, syta saephan, notifil, roseville ca 95661, ground, of 2, 214 787-430o, us, bill sender",
        "ship to, ups ground, 41 lbs, tracking : 1z v4w 195 03 6500 6276, manautr, 2821 carradale dr, ree v0084700946203420100402, etxk-0806:, 0f 1, 1, ky dong, 95661-4047, ref, wi 34.18, 17, nippina, 310 99-085, ca 956 0-01, billing pip, roseville ca, cwtainity",
    ]

    times = []
    for i, text in enumerate(test_texts[:test_cases], 1):
        print(f"\n  Test {i}/{test_cases}:")
        start = time.time()
        result = extract_with_ai(text, verbose=True)
        elapsed = time.time() - start
        times.append(elapsed)

        if result:
            print(f"    ✅ Name: {result.get('recipient_name')}")
            print(f"    ✅ Address: {result.get('address')}")
        else:
            print(f"    ❌ Extraction failed")

    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        under_2s = sum(1 for t in times if t < 2.0)

        print(f"\n📈 Performance Summary:")
        print(f"  Average: {avg_time:.2f}s")
        print(f"  Min: {min_time:.2f}s")
        print(f"  Max: {max_time:.2f}s")
        print(f"  Under 2s: {under_2s}/{len(times)} tests")

        if avg_time < 2.0:
            print(f"\n✅ SUCCESS! Average time is under 2 seconds")
            return True
        else:
            print(f"\n⚠️  Average time exceeds 2 seconds")
            print(f"💡 Recommendations:")
            print(f"   1. Set OLLAMA_KEEP_ALIVE=5m")
            print(f"   2. Ensure GPU acceleration is enabled")
            print(f"   3. Use a smaller model: llama3.2:1b")
            return False

    return False


def main():
    """Main optimization function."""
    print("🚀 OCR Label Extractor - Performance Optimization")
    print("=" * 60)
    print(f"Model: {OLLAMA_MODEL}\n")

    # Step 1: Warm up the model
    warmup_time = warmup_model(OLLAMA_MODEL)

    # Step 2: Test performance
    success = test_performance(OLLAMA_MODEL)

    print("\n" + "=" * 60)
    if success:
        print("✅ Optimization complete! Model is ready for fast inference.")
    else:
        print("⚠️  Performance optimization needed. See recommendations above.")
    print("=" * 60)

    print("\n💡 Tip: Run this script before processing large batches:")
    print("   python optimize_for_speed.py")
    print("\n💡 Or use the startup script:")
    print("   ./start.sh")


if __name__ == "__main__":
    # Run optimization
    main()
    
    # Optionally run pipeline after optimization
    print("\n🔥 Auto-warming complete. You can now run the pipeline:")
    print("   python main.py")
