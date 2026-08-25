from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    Certification,
    CurrentlyLearning,
    Education,
    Experience,
    Profile,
    Project,
    ProjectFeature,
    Skill,
    SocialLink,
)

PROFILE = dict(
    full_name="Prajin S",
    headline="Python Developer | Junior AI Engineer",
    tagline=(
        "I build AI-powered applications and Python backends — from data "
        "ingestion to a working frontend."
    ),
    summary=(
        "I'm a B.Tech Information Technology graduate with practical "
        "experience building AI-powered applications and Python-based backends "
        "using the OpenAI and Gemini APIs, FastAPI, Django, Flask, and REST API "
        "design. "
        "My projects span the full stack — sensor data pipelines, LLM-backed "
        "tools, and REST services — and I'm comfortable taking a feature from "
        "data ingestion through backend logic to frontend delivery.\n\n"
        "I got into AI engineering through building things: a resume analyzer "
        "that scores fit against a job description with the OpenAI API, a "
        "domain-specific chatbot running on OpenAI and Gemini, and an IoT "
        "attendance system that pipes sensor data through Flask into MongoDB. "
        "I'm currently deepening my prompt-engineering and API-design skills "
        "and looking for a fresher Python Developer / Junior AI Engineer role "
        "on a product-driven team building scalable, real-world AI solutions."
    ),
    looking_for=(
        "Fresher Python Developer / Junior AI Engineer roles on product-driven "
        "teams building scalable, real-world AI solutions."
    ),
    location="Coimbatore, Tamil Nadu",
    email="prajinrp6@gmail.com",
    phone="7604865376",
)

SOCIAL_LINKS = [
    dict(platform="email", label="Email", url="mailto:prajinrp6@gmail.com", order=1),
    dict(platform="phone", label="Call", url="tel:+917604865376", order=2),
    # Add GitHub / LinkedIn rows here once you have public profile URLs —
    # they appear in the nav, hero, and footer automatically.
]

EXPERIENCES = [
    dict(
        company="TechJays",
        role="Python Developer Intern",
        location="",
        timeframe="[Add dates via /admin/]",
        description=(
            "[Placeholder — add your real responsibilities and contributions "
            "at TechJays here via /admin/. Only the company and role were "
            "confirmed; nothing else about this internship is invented.]"
        ),
        technologies="Python",
        order=0,
    ),
    dict(
        company="Pantech IT Solutions",
        role="Data Science Intern",
        location="Virtual",
        timeframe="Mar 2025",
        description=(
            "Gained hands-on experience with data preprocessing, ML model "
            "workflows, and Python-based data analysis pipelines directly "
            "relevant to AI engineering tasks."
        ),
        technologies="Python, Data Preprocessing, ML Model Workflows",
        order=1,
    ),
    dict(
        company="CodTech Solutions",
        role="Cybersecurity Intern",
        location="Virtual",
        timeframe="Jun – Jul 2025",
        description=(
            "Developed Python automation scripts; strengthened backend "
            "scripting, structured delivery practices, and a security-aware "
            "development mindset."
        ),
        technologies="Python, Automation Scripting",
        order=2,
    ),
]

PROJECTS = [
    dict(
        title="IoT-Based Biometric Attendance System",
        slug="iot-biometric-attendance-system",
        timeframe="2025 – 2026",
        short_description=(
            "Real-time biometric attendance system with a Flask backend, "
            "MongoDB storage, and a live admin dashboard — final-year project."
        ),
        problem_statement=(
            "Manual attendance tracking is slow and error-prone. The project "
            "needed a real-time, hardware-integrated system that captures "
            "attendance automatically and gives admins live visibility, end to "
            "end."
        ),
        solution=(
            "Engineered a real-time biometric attendance system using "
            "fingerprint sensors (Arduino + ESP8266) paired with a Flask "
            "backend that processes sensor data and stores attendance records "
            "in MongoDB, plus a live web dashboard for admin monitoring. The "
            "system auto-marks attendance and generates daily/monthly "
            "analytical reports."
        ),
        architecture_notes=(
            "Fingerprint sensor (Arduino + ESP8266)\n"
            "Flask backend — sensor data processing\n"
            "MongoDB — attendance records\n"
            "JavaScript dashboard — live admin monitoring & reports"
        ),
        challenges=(
            "Coordinating real-time data from fingerprint hardware (Arduino + "
            "ESP8266) with a Flask backend and MongoDB so attendance is marked "
            "automatically and reliably, without duplicate or dropped reads — "
            "an end-to-end IoT + data pipeline built from scratch."
        ),
        future_improvements=(
            "Automated export of daily/monthly reports, and role-based access "
            "for admins on the dashboard."
        ),
        technologies="Python, Flask, MongoDB, Arduino, ESP8266, JavaScript",
        category="fullstack",
        featured=True,
        order=1,
        features=[
            "Auto-marks attendance from live fingerprint sensor reads",
            "Live web dashboard for admin monitoring",
            "Daily and monthly analytical attendance reports",
            "End-to-end IoT + data pipeline: sensor → backend → database → dashboard",
        ],
    ),
    dict(
        title="AI-Powered Resume Analyzer",
        slug="ai-powered-resume-analyzer",
        timeframe="Feb 2026",
        short_description=(
            "Full-stack AI app that scores an uploaded resume against a job "
            "description using the OpenAI API and NLP-based keyword matching."
        ),
        problem_statement=(
            "Job seekers need fast, structured feedback on how well a resume "
            "matches a specific job description — more useful than a plain "
            "keyword count."
        ),
        solution=(
            "Built a FastAPI backend with RESTful endpoints for PDF ingestion, "
            "NLP-based keyword extraction, and OpenAI-driven evaluation, "
            "returning structured JSON consumed by a React dashboard with "
            "dynamic score visualisation and AI-generated improvement "
            "suggestions."
        ),
        architecture_notes=(
            "React frontend — resume upload & dashboard\n"
            "FastAPI backend — REST endpoints\n"
            "PyPDF2 parsing + NLP keyword extraction\n"
            "OpenAI API — AI-driven evaluation\n"
            "Structured JSON response\n"
            "React dashboard — score visualisation & suggestions"
        ),
        challenges=(
            "Turning an unstructured resume PDF into a reliable, structured "
            "comparison against a job description — parsing text with PyPDF2, "
            "extracting keywords for skill-gap detection, and combining that "
            "with an OpenAI evaluation into one consistent job-fit score."
        ),
        future_improvements=(
            "Support DOCX uploads and let users track score improvements "
            "across resume revisions."
        ),
        technologies="Python, FastAPI, OpenAI API, NLP, PyPDF2, React",
        category="ai",
        featured=True,
        order=2,
        features=[
            "PDF resume ingestion and parsing with PyPDF2",
            "NLP-based keyword extraction and skill-gap detection",
            "OpenAI-driven job-fit scoring with structured JSON output",
            "Interactive React dashboard with score visualisation and AI suggestions",
        ],
    ),
    dict(
        title="AI Chatbot",
        slug="ai-chatbot",
        timeframe="Jan 2026",
        short_description=(
            "Domain-specific conversational chatbot integrating the OpenAI "
            "and Gemini APIs with multi-turn context management."
        ),
        problem_statement=(
            "Build a conversational assistant that stays within a specific "
            "domain and holds coherent multi-turn conversations, rather than "
            "answering every message in isolation."
        ),
        solution=(
            "Built a domain-specific chatbot integrating both the OpenAI and "
            "Gemini LLM APIs, with multi-turn context management via "
            "conversation history, tuned prompt-engineering strategies to keep "
            "responses in-domain, and deployed it as a Flask web app with a "
            "clean chat UI."
        ),
        architecture_notes=(
            "User — chat UI\n"
            "Flask backend\n"
            "Conversation history / context manager\n"
            "OpenAI API / Gemini API\n"
            "Response back to chat UI"
        ),
        challenges=(
            "Keeping multi-turn responses contextually accurate and inside the "
            "intended domain scope required deliberate prompt engineering and "
            "conversation-history management across two different LLM APIs."
        ),
        future_improvements=(
            "Persist conversations per user, and add a fallback between the "
            "two LLM providers if one is unavailable."
        ),
        technologies="Python, Flask, OpenAI API, Gemini API, HTML, CSS, JavaScript",
        category="ai",
        featured=True,
        order=3,
        features=[
            "Dual LLM integration — OpenAI and Gemini APIs",
            "Multi-turn context management via conversation history",
            "Tuned prompt engineering for accurate, in-domain responses",
            "Full frontend–backend–LLM API integration built from scratch",
        ],
    ),
    dict(
        title="URL Shortener Web App",
        slug="url-shortener-web-app",
        timeframe="Dec 2025",
        short_description=(
            "Full-stack URL shortening service with a RESTful Flask backend, "
            "MongoDB storage, and click analytics."
        ),
        problem_statement=(
            "Needed a lightweight service to generate short, trackable links "
            "with reliable redirects and click analytics."
        ),
        solution=(
            "Built a full-stack URL shortening service with a RESTful Flask "
            "backend, MongoDB storage, redirect tracking, and click analytics — "
            "demonstrating solid REST API design and CRUD principles."
        ),
        architecture_notes=(
            "Client — HTML/CSS/JS\n"
            "Flask REST API\n"
            "MongoDB — URL mapping & click data\n"
            "Redirect handler — click tracking"
        ),
        challenges=(
            "Designing a clean REST API and data model for shortening, "
            "redirecting, and tracking clicks without collisions or broken "
            "redirects."
        ),
        future_improvements="Custom short-link aliases and expiring links.",
        technologies="Python, Flask, MongoDB, HTML, CSS, JavaScript, REST API",
        category="web",
        featured=False,
        order=4,
        features=[
            "RESTful Flask backend for link creation and redirection",
            "MongoDB-backed URL storage",
            "Click analytics and redirect tracking",
        ],
    ),
]

SKILLS = {
    "ai_ml": [
        "Python (AI/ML)",
        "OpenAI API",
        "Gemini API",
        "Llama",
        "RAG",
        "NLP",
        "Prompt Engineering",
        "ML Model Workflows",
        "Data Preprocessing",
    ],
    "backend": ["Django", "FastAPI", "Node.js", "Express.js", "REST API Design"],
    "frontend": ["React.js", "JavaScript", "HTML5", "CSS3", "Responsive UI"],
    "database": ["MongoDB", "PostgreSQL", "SQL", "CRUD Operations", "JSON Handling"],
    "cloud": ["Docker", "Render", "Cloudinary", "Netlify", "GitHub Pages", "API Integration"],
    "tools": ["Git", "GitHub", "VS Code", "Postman", "Claude Code", "Docker"],
    "soft": [
        "Problem-Solving",
        "Critical Thinking",
        "Quick Learner",
        "Teamwork",
        "Adaptability",
    ],
}

EDUCATION = [
    dict(
        institution="Adithya Institute of Technology, Coimbatore, Tamil Nadu",
        degree="B.Tech",
        field="Information Technology",
        start_year=2022,
        end_year=2026,
        grade="CGPA 7.8 (up to Semester 7)",
        description=(
            "Final-year project: IoT-Based Biometric Attendance System "
            "(Python, Flask, MongoDB, Arduino, ESP8266)."
        ),
        order=1,
    ),
    dict(
        institution="NCP MPL HR Sec School, Dharapuram",
        degree="HSC",
        field="",
        start_year=2020,
        end_year=2021,
        grade="75%",
        description="",
        order=2,
    ),
    dict(
        institution="NCP MPL HR Sec School, Dharapuram",
        degree="SSLC",
        field="",
        start_year=2018,
        end_year=2020,
        grade="73%",
        description="",
        order=3,
    ),
]

CERTIFICATIONS = [
    dict(
        name="Python for Data Science & AI",
        organization="Udemy",
        issue_date="Jan 2025",
        order=1,
    ),
    dict(
        name="Web Design Fundamentals",
        organization="Udemy",
        issue_date="Jul 2025",
        order=2,
    ),
    dict(
        name="SQL Fundamentals",
        organization="GeeksforGeeks",
        issue_date="2025",
        order=3,
    ),
]

CURRENTLY_LEARNING = [
    dict(
        title="LLM Application Engineering",
        description=(
            "Deepening prompt engineering and multi-turn context design "
            "across the OpenAI and Gemini APIs, building on the AI Chatbot "
            "and Resume Analyzer projects."
        ),
        order=1,
    ),
    dict(
        title="FastAPI & REST API Design",
        description=(
            "Sharpening backend architecture and API design patterns used in "
            "the Resume Analyzer project."
        ),
        order=2,
    ),
    dict(
        title="End-to-End AI Product Delivery",
        description=(
            "Growing from prototype to production-quality delivery — data "
            "ingestion through backend logic to a polished frontend."
        ),
        order=3,
    ),
]


class Command(BaseCommand):
    help = "Seed the database with the real portfolio content (see PORTFOLIO_PLAN.md)."

    @transaction.atomic
    def handle(self, *args, **options):
        profile, _ = Profile.objects.update_or_create(
            full_name=PROFILE["full_name"], defaults=PROFILE
        )
        self.stdout.write(self.style.SUCCESS(f"Profile: {profile}"))

        for link in SOCIAL_LINKS:
            SocialLink.objects.update_or_create(
                platform=link["platform"], defaults=link
            )

        for exp in EXPERIENCES:
            Experience.objects.update_or_create(
                company=exp["company"], role=exp["role"], defaults=exp
            )

        for proj in PROJECTS:
            proj = dict(proj)
            features = proj.pop("features", [])
            project, _ = Project.objects.update_or_create(
                slug=proj["slug"], defaults=proj
            )
            project.features.all().delete()
            for i, text in enumerate(features):
                ProjectFeature.objects.create(project=project, text=text, order=i)

        for category, names in SKILLS.items():
            for i, name in enumerate(names):
                Skill.objects.update_or_create(
                    name=name, category=category, defaults={"order": i}
                )

        for edu in EDUCATION:
            Education.objects.update_or_create(
                institution=edu["institution"], degree=edu["degree"], defaults=edu
            )

        for cert in CERTIFICATIONS:
            Certification.objects.update_or_create(
                name=cert["name"], organization=cert["organization"], defaults=cert
            )

        for item in CURRENTLY_LEARNING:
            CurrentlyLearning.objects.update_or_create(
                title=item["title"], defaults=item
            )

        self.stdout.write(self.style.SUCCESS("Portfolio content seeded successfully."))
