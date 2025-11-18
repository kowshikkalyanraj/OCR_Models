from extractor import extract_entities
from tqdm import tqdm

texts = [
    "lex2 2.8 lbs, 2821 carradale dr, 95661-4047 roseville, ca, fat1, united states, zoey dong, dsm1, 0503 dsm1, tba132376390000, cycle 1, a sm1",
    "batavia stkllt, special instructiu, metr 4684 3913 8542, g, ca 8206s, 95661, o, 230, 2, paper, fedex, mps 46843913 8553, frun, 2164 n, 9622 00 19 0 000 000 0000 0 00 4684 3913 8553, 8150 sierra college blvd ste, syta saephan, notifil, roseville ca 95661, ground, of 2, 214 787-430o, us, bill sender",
    "ship to, ups ground, 41 lbs, tracking : 1z v4w 195 03 6500 6276, manautr, 2821 carradale dr, ree v0084700946203420100402, etxk-0806:, 0f 1, 1, ky dong, 95661-4047, ref, wi 34.18, 17, nippina, 310 99-085, ca 956 0-01, billing pip, roseville ca, cwtainity",
    "tba098191199000, a, 2821 carradale dr, united states, 0426 dsm1, 95661 -4047 roseville, ca, lex2 1.7 lbs, smf1, sm1, dpuxb7pivsecandit of 22, ryan dong, dsm1, cycle 1",
    "ship to, ontrac, ky dong, ctiei33869492, sac, lbs: 4, 2821 carradale dr, ground, ontrac.com, roseville, ca 95661-0000, nagteapn arte ny, 800.334.5000",
    "p, priority mail 3-day, 9410 8118 9900 q302 29290, usps sgnatuire tracxing, notifw llc, alphareta ga 30005-e, roseville ca s5b61, 8190 srra college blid site 21, 800 north point panky sut, lalarry andersan",
    "p, priority mail 3-day, 9410 8118 9900 q302 29290, usps sgnatuire tracxing, notifw llc, alphareta ga 30005-e, roseville ca s5b61, 8190 srra college blid site 21, 800 north point panky sut, lalarry andersan"
]

output = extract_entities(texts)

print("\n✅ FINAL EXTRACTED RESULTS:")
print("=" * 60)
for idx, res in enumerate(tqdm(output["Results"], desc="Processing")):
    print(f"✅ Record {idx+1}:")
    print(f"   Name: {res['Name'] or 'None'}")
    print(f"   Address: {res['Address'] or 'None'}")
    print(f"   Tracking: {res['TrackingNumber'] or 'None'}\n")
print("=" * 60)
print("📁 Results also saved to: final_extracted_results.json\n")
