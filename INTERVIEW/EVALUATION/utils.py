import json
from datetime import datetime

def present_to_user(msg: str):
    print(msg)

def clean_json(raw: str) -> dict:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[len("json"):].strip()
        cleaned = cleaned.strip("`").strip()
    try:
        return json.loads(cleaned)
    except Exception as e:
        print(f"⚠️ JSON parsing failed: {e}")
        return {}
    
def export_state(state: dict, folder: str = "logs") -> str:
    """
    Save interview state to a JSON file.
    Returns the file path.
    """
    import os
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    company = state.get("company_name", "UnknownCompany").replace(" ", "_")
    filename = f"{folder}/interview_{company}_{timestamp}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

    return filename
