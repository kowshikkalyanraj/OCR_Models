import json
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "microsoft/phi-2"

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype="auto",
    device_map="cpu"
)

print("Model loaded.")

# Read raw text file
with open("raw.txt", "r", encoding="utf-8") as f:
    lines = json.load(f)

def build_prompt(text):
    return f"""
Extract the destination recipient (the person or location the parcel is being SENT TO).
Correct OCR mistakes. Fix city/state/ZIP if needed.
Return valid JSON like:
{{
  "Name": "...",
  "Address": "...",
  "TrackingNumber": "..."
}}

Text:
{text}

Answer:
"""

def run_model(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=200,
        temperature=0.2
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

results = []

for raw in lines:
    prompt = build_prompt(raw)
    output = run_model(prompt)

    # Extract JSON part
    try:
        json_start = output.index("{")
        json_end = output.rindex("}") + 1
        parsed = json.loads(output[json_start:json_end])
        results.append(parsed)
    except:
        results.append({"error": output})

# save results
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nDONE! Check results.json")
