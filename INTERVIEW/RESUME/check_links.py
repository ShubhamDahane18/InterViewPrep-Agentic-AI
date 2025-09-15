import requests
from INTERVIEW.RESUME.state import ResumeAgentState

def check_links_and_alert(state: ResumeAgentState) -> ResumeAgentState:
    broken_links = []
    
    for key, value in state.items():
        if key in ("full_text", "links"):
            continue
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for k, v in item.items():
                        if isinstance(v, str) and v.startswith("http"):
                            try:
                                response = requests.get(v, timeout=5)
                                if response.status_code >= 400:
                                    broken_links.append((k, v, response.status_code))
                            except Exception:
                                broken_links.append((k, v, "Error"))
        elif isinstance(value, str) and value.startswith("http"):
            try:
                response = requests.get(value, timeout=5)
                if response.status_code >= 400:
                    broken_links.append((key, value, response.status_code))
            except Exception:
                broken_links.append((key, value, "Error"))

    if broken_links:
        msg = "🚨 Some links in your resume are not working:\n"
        for k, link, status in broken_links:
            msg += f"- **Key**: `{k}` | **Link**: {link} | **Status**: {status}\n"
        msg += "\n🔁 Please update these links in your resume."
    else:
        msg = "✅ All good! All details are fetched successfully and your links are working fine."

    return {"message":msg}