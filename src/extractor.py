import re
import time
import json
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

def extract_entities(texts):
    start_time = time.time()
    results = []

    model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    for text in texts:
        clean_start = time.time()
        cleaned_text = text.strip()

        entities = nlp(cleaned_text)

        # Improved Name extraction
        names = [ent['word'] for ent in entities if ent['entity_group'] == 'PER']
        name = ", ".join(names).title() if names else None


        # Improved Tracking number extraction
        tracking_match = re.search(
            r'\b(?:1Z(?:[\s-]?[0-9A-Z]){8,20}|TBA(?:[\s-]?[0-9A-Z]){8,20}|9(?:[\s-]?[0-9]){15,22})\b',
            cleaned_text,
            re.IGNORECASE
        )
        tracking_number = re.sub(r'[\s-]', '', tracking_match.group(0)).upper() if tracking_match else None

        # Improved Address extraction
        address_match = re.search(
            r'(\d{1,5}\s+[\w\s,.]+?,\s*[\w\s]+?,\s*[A-Za-z]{2,}\s*\d{5}(?:-\d{4})?)',
            cleaned_text,
            re.IGNORECASE
        )
        address = address_match.group(1).strip().title() if address_match else None

        clean_end = time.time()
        results.append({
            "Name": name,
            "Address": address,
            "TrackingNumber": tracking_number,
            "CleanedText": cleaned_text,
            "TimeTaken": round(clean_end - clean_start, 3)
        })

    total_time = time.time() - start_time

    final_output = {
        "Total_Texts_Processed": len(texts),
        "Total_Execution_Time_Seconds": round(total_time, 3),
        "Results": results
    }

    # Save to JSON file automatically
    with open("final_extracted_results.json", "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=4, ensure_ascii=False)

    return final_output
