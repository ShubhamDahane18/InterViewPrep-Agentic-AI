from typing import TypedDict, Optional, List
from typing_extensions import NotRequired


class Project(TypedDict):
    project_name: Optional[str]
    github_link: NotRequired[Optional[str]]
    live_link: NotRequired[Optional[str]]
    time_period: NotRequired[Optional[str]]
    features: NotRequired[List[str]]
    tech_stack: NotRequired[List[str]]


class SkillsSection(TypedDict):
    programming_languages: NotRequired[List[str]]
    frameworks: NotRequired[List[str]]
    libraries_tools: NotRequired[List[str]]
    databases: NotRequired[List[str]]
    soft_skills: NotRequired[List[str]]


class Experience(TypedDict):
    role: Optional[str]
    company: Optional[str]
    start_date: NotRequired[Optional[str]]
    end_date: NotRequired[Optional[str]]
    responsibilities: NotRequired[List[str]]


class ExtracurricularActivity(TypedDict):
    title: Optional[str]
    organization: NotRequired[Optional[str]]
    description: NotRequired[Optional[str]]
    date: NotRequired[Optional[str]]


class ResumeAgentState(TypedDict):
    message: NotRequired[Optional[str]]
    full_text: NotRequired[Optional[str]]
    links: NotRequired[List[dict]]

    # Personal Info
    name: NotRequired[Optional[str]]
    email: NotRequired[Optional[str]]
    mob_no: NotRequired[Optional[str]]

    # Profile Links
    linkedin: NotRequired[Optional[str]]
    github: NotRequired[Optional[str]]
    leetcode: NotRequired[Optional[str]]

    # Skills and Projects
    skills: NotRequired[SkillsSection]
    projects: NotRequired[List[Project]]

    # Experience and Extracurriculars
    experience: NotRequired[List[Experience]]
    extracurriculars: NotRequired[List[ExtracurricularActivity]]


# job_state.py
class JobInfoState(TypedDict):
    response: Optional[str]
    user_input: Optional[str]
    job_title: Optional[str]
    company: Optional[str]
    location: NotRequired[Optional[str]]
    job_type: NotRequired[Optional[str]]  # Full-time, Internship, etc.
    description: NotRequired[Optional[str]]
    required_skills: NotRequired[List[str]]
