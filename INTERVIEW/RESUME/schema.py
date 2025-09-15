from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class Project(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    github_link: Optional[str] = Field(None, description="GitHub URL of the project")
    live_link: Optional[str] = Field(None, description="Live demo or deployment link")
    time_period: Optional[str] = Field(None, description="Time duration or dates of the project")
    features: Optional[List[str]] = Field(default_factory=list, description="Key features of the project")
    tech_stack: Optional[List[str]] = Field(default_factory=list, description="Technologies used in the project")


class SkillsSection(BaseModel):
    programming_languages: Optional[List[str]] = Field(default_factory=list, description="Languages like Python, C++")
    frameworks: Optional[List[str]] = Field(default_factory=list, description="Frameworks like Django, React")
    libraries_tools: Optional[List[str]] = Field(default_factory=list, description="Libraries and tools like NumPy, Git")
    databases: Optional[List[str]] = Field(default_factory=list, description="Databases like MongoDB, MySQL")
    soft_skills: Optional[List[str]] = Field(default_factory=list, description="Soft skills like leadership, communication")


class Experience(BaseModel):
    role: str = Field(..., description="Job title or position held")
    company: str = Field(..., description="Company or organization name")
    start_date: Optional[str] = Field(None, description="Start date in format YYYY-MM or similar")
    end_date: Optional[str] = Field(None, description="End date or 'Present'")
    responsibilities: Optional[List[str]] = Field(default_factory=list, description="Key responsibilities or achievements")


class ExtracurricularActivity(BaseModel):
    title: str = Field(..., description="Name of the activity or achievement")
    organization: Optional[str] = Field(None, description="Organization or club involved")
    description: Optional[str] = Field(None, description="Details of the activity")
    date: Optional[str] = Field(None, description="Date or time period of the activity")


class ExtractResumeData(BaseModel):
    # Personal Information
    name: Optional[str] = Field(None, description="Candidate's full name")
    email: Optional[EmailStr] = Field(None, description="Email address")
    mob_no: Optional[str] = Field(None, description="Mobile phone number")

    # Profiles
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    leetcode: Optional[str] = Field(None, description="LeetCode profile URL")

    # Skills and Projects
    skills: Optional[SkillsSection] = Field(default_factory=SkillsSection, description="Structured skill information")
    projects: Optional[List[Project]] = Field(default_factory=list, description="List of personal or academic projects")

    # New Sections
    experience: Optional[List[Experience]] = Field(default_factory=list, description="Work or internship experience")
    extracurriculars: Optional[List[ExtracurricularActivity]] = Field(default_factory=list, description="Clubs, competitions, and other activities")


class ExtractJobInfo(BaseModel):
    job_title: str = Field(..., description="Title of the job role, e.g., Software Engineer, Data Analyst")
    company: Optional[str] = Field(None, description="Name of the company offering the job")
    location: Optional[str] = Field(None, description="Job location, e.g., city, state, or remote")
    job_type: Optional[str] = Field(None, description="Type of job, e.g., Full-time, Internship, Contract")
    description: Optional[str] = Field(None, description="Full job description text")
    required_skills: List[str] = Field(default_factory=list, description="List of skills required for the job role")