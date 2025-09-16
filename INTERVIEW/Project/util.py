import requests

def fetch_github_readme(repo_url: str) -> str | None:
    """
    Fetch README.md content from a GitHub repo.
    repo_url: "https://github.com/username/repo"
    """
    try:
        parts = repo_url.rstrip("/").split("/")
        owner, repo = parts[-2], parts[-1]

        # GitHub raw URL
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
        resp = requests.get(raw_url, timeout=10)

        if resp.status_code == 200:
            return resp.text
        else:
            return None
    except Exception:
        return None

def enrich_resume_projects(email: str) -> HRState:
    """
    Fetch resume projects, pull GitHub READMEs, and update HRState.projects.
    """
    state = get_hr_state(email)
    if not state:
        state = HRState()
    
    if not state.resume_info or "projects" not in state.resume_info:
        return state  # nothing to enrich

    projects = state.resume_info.get("projects", [])
    enriched_projects = []

    for project in projects:
        repo_url = project.get("github_link")
        readme = fetch_github_readme(repo_url) if repo_url else None
        enriched_projects.append({**project, "readme": readme})

    # Update state with enriched projects
    state.resume_info["projects"] = enriched_projects
    save_hr_state(email, state)
    return state