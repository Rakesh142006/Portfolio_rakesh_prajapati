from datetime import date
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Profile, Skill, Project, Certificate, Experience


class Command(BaseCommand):
    help = "Seed the database with Rakesh Prajapati's portfolio content."

    def handle(self, *args, **options):
        profile, _ = Profile.objects.get_or_create(pk=1)
        profile.full_name = "Rakesh Prajapati"
        profile.tagline = "Python Developer"
        profile.bio = (
            "I'm a Python Developer with hands-on experience building backend systems "
            "using Django, Flask, and REST APIs, along with relational database design "
            "in MySQL and SQLite, and practical exposure to data extraction and parsing. "
            "I'm comfortable working across the full stack — integrating server-side "
            "logic with front-end components (HTML5, CSS3, JavaScript) — and "
            "collaborating with cross-functional teams to deliver testable, "
            "maintainable code.\n\n"
            "I'm currently a Python Intern at Code Vibe Innovation, where I've "
            "delivered projects including Baby Sitter Club, AI Resume Analyzer, and "
            "Expense Tracker. I'm available to join immediately as a full-time Python "
            "Developer."
        )
        profile.email = "rkp97840036@gmail.com"
        profile.phone = "+91-9327761902"
        profile.location = "Ahmedabad, Gujarat"
        profile.linkedin_url = "https://www.linkedin.com/in/rakeshprajapati-ab7776360"
        profile.education = "BCA (Honors) — Shreyarth University, Ahmedabad (Expected May 2026)"
        profile.years_experience = 1

        resume_path = settings.BASE_DIR / "media" / "resume" / "Rakesh_Prajapati_Resume.pdf"
        if resume_path.exists() and not profile.resume:
            with open(resume_path, "rb") as f:
                profile.resume.save("Rakesh_Prajapati_Resume.pdf", File(f), save=False)

        profile.save()

        skills_data = [
            ("Python", "language", 88),
            ("JavaScript", "language", 65),
            ("SQL", "language", 78),
            ("Django", "framework", 85),
            ("Flask", "framework", 75),
            ("Django REST Framework", "framework", 78),
            ("Bootstrap", "framework", 78),
            ("MySQL", "database", 75),
            ("SQLite", "database", 80),
            ("PostgreSQL", "database", 55),
            ("HTML5 & CSS3", "tool", 80),
            ("Git & GitHub", "tool", 80),
            ("Requests & BeautifulSoup", "tool", 68),
            ("Selenium", "tool", 40),
            ("n8n", "tool", 60),
            ("Render", "tool", 55),
        ]
        for i, (name, cat, prof) in enumerate(skills_data):
            Skill.objects.update_or_create(
                name=name, defaults={"category": cat, "proficiency": prof, "order": i}
            )

        projects_data = [
            {
                "title": "Baby Sitter Club Management System",
                "summary": "A web-based babysitting management platform with booking and profile management.",
                "description": (
                    "Developed a web-based babysitting management platform with "
                    "authentication, booking, and profile management.\n\n"
                    "Implemented CRUD operations and server-side logic using Django, "
                    "Bootstrap, and SQLite."
                ),
                "tech_stack": "Django, Bootstrap, SQLite",
                "featured": True,
            },
            {
                "title": "AI Resume Analyzer",
                "summary": "An AI-powered resume analysis system with ATS scoring and automated notifications.",
                "description": (
                    "Built an AI-powered resume analysis system with ATS scoring and "
                    "automated email notifications via n8n.\n\n"
                    "Integrated the Gemini API and designed the database schema for "
                    "resume upload, report generation, and dashboards."
                ),
                "tech_stack": "Flask, SQLite, Gemini API, n8n",
                "featured": True,
            },
            {
                "title": "Expense Tracker Website",
                "summary": "An expense tracking system with authentication and a reporting dashboard.",
                "description": (
                    "Developed an expense tracking system with authentication, and "
                    "income/expense/category management.\n\n"
                    "Built CRUD operations and a reporting dashboard using Django and "
                    "SQLite."
                ),
                "tech_stack": "Django, Bootstrap, SQLite",
                "featured": True,
            },
        ]
        for i, data in enumerate(projects_data):
            Project.objects.update_or_create(
                title=data["title"], defaults={**data, "order": i}
            )

        certs_data = [
            ("IBM SkillsBuild AI Strategy & Business Intelligence Internship", "IBM SkillsBuild", date(2026, 6, 1)),
            ("Tata GenAI Powered Data Analytics Job Simulation", "Tata (via Forage)", date(2026, 4, 1)),
            ("Web Development with Python Django", "Techmicra", date(2025, 6, 1)),
        ]
        for i, (title, issuer, d) in enumerate(certs_data):
            Certificate.objects.update_or_create(
                title=title, defaults={"issuer": issuer, "issue_date": d, "order": i}
            )

        experiences_data = [
            {
                "role": "Python Intern",
                "company": "Code Vibe Innovation",
                "location": "Ahmedabad",
                "start_date": date(2026, 4, 1),
                "end_date": None,
                "is_current": True,
                "description": (
                    "Develop and maintain back-end components and REST APIs using "
                    "Python and Django, improving application responsiveness and "
                    "performance.\n"
                    "Design database schemas and implement CRUD operations and "
                    "authentication systems following coding standards and "
                    "documentation practices.\n"
                    "Debug and troubleshoot existing applications, collaborating with "
                    "team members to resolve issues and improve project outcomes."
                ),
            },
            {
                "role": "Web Development Intern",
                "company": "Techmicra",
                "location": "Ahmedabad",
                "start_date": date(2025, 5, 1),
                "end_date": date(2025, 6, 30),
                "is_current": False,
                "description": (
                    "Built Django applications with CRUD functionality and SQL "
                    "integration, writing reusable and testable code.\n"
                    "Used Git and GitHub for version control and collaborated with "
                    "the team throughout the development lifecycle."
                ),
            },
        ]
        for i, data in enumerate(experiences_data):
            Experience.objects.update_or_create(
                role=data["role"], company=data["company"], defaults={**data, "order": i}
            )

        self.stdout.write(self.style.SUCCESS("Rakesh's portfolio data seeded successfully."))
