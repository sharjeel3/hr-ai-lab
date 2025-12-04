"""
Synthetic Data Generator for HR AI Lab

This script generates realistic synthetic datasets for HR AI experiments including:
- CVs for recruitment screening
- Interview transcripts
- Performance review notes
- Job family definitions
- HRIS employee records

Usage:
    python generate_datasets.py --all
    python generate_datasets.py --cvs 20
    python generate_datasets.py --interviews 10
    python generate_datasets.py --performance 15
"""

import json
import random
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# Base directories
BASE_DIR = Path(__file__).parent.parent / "datasets"
CV_DIR = BASE_DIR / "synthetic_cvs"
INTERVIEW_DIR = BASE_DIR / "interview_transcripts"
PERFORMANCE_DIR = BASE_DIR / "performance_notes"
JOB_FAMILIES_DIR = BASE_DIR / "job_families"
HRIS_DIR = BASE_DIR / "hris_samples"


class DataGenerator:
    """Base class for generating synthetic HR data"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.first_names = [
            "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
            "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
            "Thomas", "Sarah", "Carlos", "Maria", "Mohammed", "Fatima", "Wei", "Yuki",
            "Raj", "Priya", "Ahmed", "Aisha", "Kim", "Chen", "Alex", "Sam"
        ]
        self.last_names = [
            "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
            "Rodriguez", "Martinez", "Wilson", "Anderson", "Taylor", "Thomas", "Moore",
            "Jackson", "Martin", "Lee", "Thompson", "White", "Kim", "Chen", "Patel",
            "Singh", "Wong", "Ali", "Khan", "Nguyen", "Okonkwo", "Santos", "Silva"
        ]
        
    def generate_name(self) -> tuple:
        """Generate a random first and last name"""
        return random.choice(self.first_names), random.choice(self.last_names)
    
    def generate_email(self, first_name: str, last_name: str) -> str:
        """Generate email address"""
        return f"{first_name.lower()}.{last_name.lower()}@email.com"
    
    def generate_phone(self) -> str:
        """Generate US phone number"""
        return f"+1-555-{random.randint(1000, 9999)}"


class CVGenerator(DataGenerator):
    """Generate synthetic CV/resume data"""
    
    PROGRAMMING_LANGUAGES = [
        "Python", "JavaScript", "TypeScript", "Java", "Go", "Rust",
        "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin", "Scala"
    ]
    
    FRAMEWORKS = [
        "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI",
        "Spring Boot", "Node.js", "Express", ".NET Core", "Rails"
    ]
    
    TOOLS = [
        "Docker", "Kubernetes", "AWS", "GCP", "Azure", "Git", "Jenkins",
        "PostgreSQL", "MongoDB", "Redis", "Kafka", "Elasticsearch"
    ]
    
    COMPANIES = [
        "TechCorp Inc.", "DataSolutions LLC", "CloudPlatform Inc.",
        "InnovateSoft", "Digital Dynamics", "StartupX", "Enterprise Systems"
    ]
    
    CITIES = [
        "San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX",
        "Boston, MA", "Chicago, IL", "Denver, CO", "Los Angeles, CA"
    ]
    
    def generate_cv(self, cv_id: int, level: str = "mid") -> Dict[str, Any]:
        """Generate a complete CV"""
        first_name, last_name = self.generate_name()
        
        if level == "junior":
            years_exp = random.randint(0, 2)
            num_jobs = random.randint(1, 2)
        elif level == "mid":
            years_exp = random.randint(3, 7)
            num_jobs = random.randint(2, 3)
        else:  # senior
            years_exp = random.randint(8, 15)
            num_jobs = random.randint(3, 5)
        
        cv = {
            "candidate_id": f"CV{cv_id:03d}",
            "name": f"{first_name} {last_name}",
            "email": self.generate_email(first_name, last_name),
            "phone": self.generate_phone(),
            "location": random.choice(self.CITIES),
            "summary": self._generate_summary(years_exp, level),
            "experience": self._generate_experience(num_jobs, years_exp),
            "education": self._generate_education(),
            "skills": self._generate_skills(level),
            "languages": [
                {"language": "English", "proficiency": "Fluent"}
            ]
        }
        
        return cv
    
    def _generate_summary(self, years: int, level: str) -> str:
        summaries = {
            "junior": f"Recent graduate with {years} year{'s' if years != 1 else ''} of experience in software development.",
            "mid": f"Software Engineer with {years} years of experience building scalable applications.",
            "senior": f"Senior Engineer with {years}+ years of experience leading technical teams and architecting systems."
        }
        return summaries.get(level, summaries["mid"])
    
    def _generate_experience(self, num_jobs: int, total_years: int) -> List[Dict]:
        experience = []
        current_date = datetime.now()
        years_allocated = 0
        
        for i in range(num_jobs):
            is_current = (i == 0)
            years_at_company = random.randint(1, min(4, total_years - years_allocated + 1))
            
            if is_current:
                start_date = current_date - timedelta(days=365 * years_at_company)
                end_date = "present"
            else:
                end_date = current_date - timedelta(days=365 * years_allocated)
                start_date = end_date - timedelta(days=365 * years_at_company)
            
            job = {
                "title": random.choice(["Software Engineer", "Senior Engineer", "Developer", "Tech Lead"]),
                "company": random.choice(self.COMPANIES),
                "location": random.choice(self.CITIES),
                "start_date": start_date.strftime("%Y-%m") if isinstance(start_date, datetime) else start_date,
                "end_date": end_date if end_date == "present" else end_date.strftime("%Y-%m"),
                "responsibilities": [
                    "Developed scalable web applications",
                    "Collaborated with cross-functional teams",
                    "Implemented new features and fixed bugs",
                    "Participated in code reviews and agile ceremonies"
                ]
            }
            experience.append(job)
            years_allocated += years_at_company
        
        return experience
    
    def _generate_education(self) -> List[Dict]:
        degrees = ["Bachelor of Science", "Bachelor of Arts", "Master of Science"]
        majors = ["Computer Science", "Software Engineering", "Information Technology"]
        
        return [{
            "degree": f"{random.choice(degrees)} in {random.choice(majors)}",
            "institution": "State University",
            "graduation_year": str(random.randint(2010, 2024)),
            "gpa": f"{random.uniform(3.0, 4.0):.1f}/4.0"
        }]
    
    def _generate_skills(self, level: str) -> Dict[str, List[str]]:
        num_languages = 3 if level == "junior" else (5 if level == "mid" else 7)
        num_frameworks = 2 if level == "junior" else (4 if level == "mid" else 6)
        
        return {
            "programming_languages": random.sample(self.PROGRAMMING_LANGUAGES, min(num_languages, len(self.PROGRAMMING_LANGUAGES))),
            "frameworks": random.sample(self.FRAMEWORKS, min(num_frameworks, len(self.FRAMEWORKS))),
            "tools": random.sample(self.TOOLS, random.randint(4, 8)),
            "soft_skills": ["Problem Solving", "Team Collaboration", "Communication", "Adaptability"]
        }


class InterviewGenerator(DataGenerator):
    """Generate synthetic interview transcripts"""
    
    def generate_interview(self, interview_id: int, candidate_cv: Dict = None) -> Dict[str, Any]:
        """Generate interview transcript"""
        candidate_name = candidate_cv["name"] if candidate_cv else f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
        
        interview = {
            "interview_id": f"INT{interview_id:03d}",
            "candidate_name": candidate_name,
            "candidate_id": candidate_cv["candidate_id"] if candidate_cv else f"CV{interview_id:03d}",
            "position": random.choice(["Software Engineer", "Senior Engineer", "Product Manager", "Data Scientist"]),
            "interviewer": f"{random.choice(self.first_names)} {random.choice(self.last_names)} (Hiring Manager)",
            "date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
            "duration_minutes": random.randint(30, 60),
            "interview_type": random.choice(["Technical", "Behavioral", "Technical + Behavioral"]),
            "transcript": self._generate_transcript(),
            "notes": self._generate_notes(),
            "rating": self._generate_rating(),
            "recommendation": random.choice([
                "Strong hire",
                "Hire",
                "Maybe - need more signal",
                "No hire"
            ])
        }
        
        return interview
    
    def _generate_transcript(self) -> List[Dict]:
        """Generate sample interview dialogue"""
        return [
            {
                "speaker": "Interviewer",
                "timestamp": "00:00",
                "text": "Thanks for joining us today. Can you tell me about your background?"
            },
            {
                "speaker": "Candidate",
                "timestamp": "00:10",
                "text": "Sure, I have been working as a software engineer for the past few years, focusing on backend development and API design."
            },
            {
                "speaker": "Interviewer",
                "timestamp": "00:30",
                "text": "Great. Can you walk me through a challenging technical problem you've solved recently?"
            },
            {
                "speaker": "Candidate",
                "timestamp": "00:45",
                "text": "Recently, I optimized a database query that was causing performance issues. I analyzed the execution plan, added appropriate indexes, and reduced query time by 70%."
            }
        ]
    
    def _generate_notes(self) -> Dict[str, str]:
        return {
            "technical_skills": random.choice(["Strong", "Good", "Adequate", "Weak"]),
            "communication": random.choice(["Excellent", "Good", "Adequate", "Poor"]),
            "culture_fit": random.choice(["Excellent fit", "Good fit", "Uncertain", "Concerns"])
        }
    
    def _generate_rating(self) -> Dict[str, float]:
        overall = round(random.uniform(2.0, 5.0), 1)
        return {
            "technical": round(random.uniform(2.0, 5.0), 1),
            "communication": round(random.uniform(2.0, 5.0), 1),
            "problem_solving": round(random.uniform(2.0, 5.0), 1),
            "overall": overall
        }


class PerformanceNoteGenerator(DataGenerator):
    """Generate synthetic performance review notes"""
    
    def generate_performance_note(self, note_id: int) -> Dict[str, Any]:
        first_name, last_name = self.generate_name()
        
        performance_level = random.choice(["high", "good", "average", "needs_improvement"])
        
        note = {
            "performance_note_id": f"PN{note_id:03d}",
            "employee_id": f"EMP{random.randint(1000, 9999)}",
            "employee_name": f"{first_name} {last_name}",
            "position": random.choice([
                "Software Engineer", "Product Manager", "Data Analyst",
                "Designer", "Marketing Manager", "Sales Representative"
            ]),
            "manager": f"{random.choice(self.first_names)} {random.choice(self.last_names)}",
            "review_period": "2024 Q3-Q4",
            "date_created": datetime.now().strftime("%Y-%m-%d"),
            "notes": self._generate_observations(performance_level),
            "overall_performance": self._get_performance_label(performance_level),
            "recommended_rating": f"{random.uniform(2.0, 5.0):.1f}/5"
        }
        
        return note
    
    def _generate_observations(self, level: str) -> List[Dict]:
        observations = []
        
        if level == "high":
            observations = [
                {
                    "date": "2024-09-15",
                    "category": "Achievement",
                    "observation": "Completed major project ahead of schedule with exceptional quality."
                },
                {
                    "date": "2024-10-20",
                    "category": "Leadership",
                    "observation": "Mentored junior team members and helped improve team productivity."
                }
            ]
        elif level == "needs_improvement":
            observations = [
                {
                    "date": "2024-09-10",
                    "category": "Quality Concern",
                    "observation": "Deliverables required multiple rounds of revisions."
                },
                {
                    "date": "2024-10-15",
                    "category": "Communication",
                    "observation": "Missed important deadlines without proactive communication."
                }
            ]
        else:
            observations = [
                {
                    "date": "2024-09-12",
                    "category": "Performance",
                    "observation": "Met baseline expectations for assigned tasks."
                }
            ]
        
        return observations
    
    def _get_performance_label(self, level: str) -> str:
        labels = {
            "high": "Exceeds Expectations",
            "good": "Meets Expectations",
            "average": "Meets Expectations",
            "needs_improvement": "Needs Improvement"
        }
        return labels.get(level, "Meets Expectations")


def generate_all_datasets(num_cvs: int = 10, num_interviews: int = 5, num_performance: int = 5):
    """Generate all synthetic datasets"""
    
    print("🚀 Starting synthetic data generation...")
    
    # Create directories if they don't exist
    for dir_path in [CV_DIR, INTERVIEW_DIR, PERFORMANCE_DIR]:
        dir_path.mkdir(parents=True, exist_ok=True)
    
    # Generate CVs
    print(f"\n📄 Generating {num_cvs} CVs...")
    cv_generator = CVGenerator()
    cvs = []
    
    for i in range(1, num_cvs + 1):
        level = random.choice(["junior", "mid", "senior"])
        cv = cv_generator.generate_cv(i, level)
        cvs.append(cv)
        
        filename = f"cv_{i:03d}_{level}.json"
        with open(CV_DIR / filename, 'w') as f:
            json.dump(cv, f, indent=2)
    
    print(f"✅ Generated {num_cvs} CVs in {CV_DIR}")
    
    # Generate Interviews
    print(f"\n🎤 Generating {num_interviews} interview transcripts...")
    interview_generator = InterviewGenerator()
    
    for i in range(1, num_interviews + 1):
        # Use some CVs if available
        candidate_cv = cvs[i-1] if i <= len(cvs) else None
        interview = interview_generator.generate_interview(i, candidate_cv)
        
        filename = f"interview_{i:03d}.json"
        with open(INTERVIEW_DIR / filename, 'w') as f:
            json.dump(interview, f, indent=2)
    
    print(f"✅ Generated {num_interviews} interviews in {INTERVIEW_DIR}")
    
    # Generate Performance Notes
    print(f"\n📊 Generating {num_performance} performance notes...")
    perf_generator = PerformanceNoteGenerator()
    
    for i in range(1, num_performance + 1):
        note = perf_generator.generate_performance_note(i)
        
        filename = f"perf_note_{i:03d}.json"
        with open(PERFORMANCE_DIR / filename, 'w') as f:
            json.dump(note, f, indent=2)
    
    print(f"✅ Generated {num_performance} performance notes in {PERFORMANCE_DIR}")
    
    print("\n✨ Dataset generation complete!")
    print(f"\nDatasets location: {BASE_DIR}")


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic HR datasets")
    parser.add_argument("--all", action="store_true", help="Generate all datasets")
    parser.add_argument("--cvs", type=int, default=10, help="Number of CVs to generate")
    parser.add_argument("--interviews", type=int, default=5, help="Number of interviews to generate")
    parser.add_argument("--performance", type=int, default=5, help="Number of performance notes to generate")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility")
    
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    if args.all or not any([args.cvs, args.interviews, args.performance]):
        generate_all_datasets(args.cvs, args.interviews, args.performance)
    else:
        print("Use --all flag or specify individual dataset counts")


if __name__ == "__main__":
    main()
