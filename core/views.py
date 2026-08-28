import json
import urllib.error
import urllib.request

from django.conf import settings
from django.http import Http404, FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from .forms import ContactForm
from .models import (
    Certification,
    CurrentlyLearning,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
)


def _resume_path():
    path = settings.MEDIA_ROOT / "resume" / settings.RESUME_FILE_NAME
    return path if path.exists() else None


def _github_snapshot():
    """Best-effort GitHub activity fetch. Returns None if no username is
    configured or the API call fails for any reason — the template hides
    the whole section rather than showing broken data."""
    username = settings.GITHUB_USERNAME
    if not username:
        return None
    try:
        request = urllib.request.Request(
            f"https://api.github.com/users/{username}",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "portfolio-site"},
        )
        with urllib.request.urlopen(request, timeout=3) as response:
            data = json.loads(response.read().decode())
        repos_request = urllib.request.Request(
            f"https://api.github.com/users/{username}/repos?sort=updated&per_page=6",
            headers={"Accept": "application/vnd.github+json", "User-Agent": "portfolio-site"},
        )
        with urllib.request.urlopen(repos_request, timeout=3) as response:
            repos = json.loads(response.read().decode())
        return {
            "username": username,
            "public_repos": data.get("public_repos"),
            "followers": data.get("followers"),
            "profile_url": data.get("html_url", f"https://github.com/{username}"),
            "repos": [
                {
                    "name": r.get("name"),
                    "url": r.get("html_url"),
                    "description": r.get("description"),
                    "language": r.get("language"),
                    "stars": r.get("stargazers_count", 0),
                }
                for r in repos
                if not r.get("private")
            ][:6],
        }
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError):
        return None


def home(request):
    return render(request, "core/home.html", _home_context())


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.exclude(pk=project.pk).filter(category=project.category)[:3]
    return render(
        request,
        "core/project_detail.html",
        {"project": project, "related_projects": related},
    )


@require_http_methods(["GET", "POST"])
def contact(request):
    """Handles both a JS fetch() submission (JSON) and a plain form POST
    fallback if JavaScript is unavailable."""
    if request.method == "POST":
        form = ContactForm(request.POST)
        wants_json = request.headers.get("x-requested-with") == "XMLHttpRequest" or (
            "application/json" in request.headers.get("accept", "")
        )
        if form.is_valid():
            form.save()
            if wants_json:
                return JsonResponse({"ok": True, "message": "Thanks — your message has been sent."})
            return render(
                request,
                "core/home.html",
                _home_context(contact_success=True),
            )
        if wants_json:
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)
        return render(request, "core/home.html", _home_context(contact_form=form))
    return render(request, "core/home.html", _home_context())


def _home_context(**overrides):
    profile = Profile.objects.first()
    experiences = Experience.objects.all()
    projects = Project.objects.all()
    skills = Skill.objects.all()
    skills_by_category = {}
    for skill in skills:
        skills_by_category.setdefault(skill.category, []).append(skill)
    education = Education.objects.all()
    certifications = Certification.objects.all()
    currently_learning = CurrentlyLearning.objects.all()
    context = {
        "profile": profile,
        "experiences": experiences,
        "projects": projects,
        "featured_projects": projects.filter(featured=True) or projects[:3],
        "skills_by_category": skills_by_category,
        "skill_categories": Skill.CATEGORY_CHOICES,
        "education": education,
        "certifications": certifications,
        "currently_learning": currently_learning,
        "snapshot": {
            "projects_count": projects.count(),
            "internships_count": experiences.count(),
            "technologies_count": skills.count(),
            "current_education": education.first(),
        },
        "contact_form": ContactForm(),
        "github": _github_snapshot(),
        "resume_available": _resume_path() is not None,
        "project_categories": Project.CATEGORY_CHOICES,
    }
    context.update(overrides)
    return context


@require_GET
def resume_view(request):
    path = _resume_path()
    if not path:
        raise Http404("Resume not uploaded yet.")
    return FileResponse(open(path, "rb"), content_type="application/pdf")


@require_GET
def resume_download(request):
    path = _resume_path()
    if not path:
        raise Http404("Resume not uploaded yet.")
    return FileResponse(open(path, "rb"), as_attachment=True, filename="Prajin-S-Resume.pdf")


# --- Lightweight read-only JSON API (no DRF — simple reads don't need it) ---

def api_projects(request):
    data = [
        {
            "title": p.title,
            "slug": p.slug,
            "category": p.category,
            "short_description": p.short_description,
            "technologies": p.technology_list,
            "github_url": p.github_url,
            "live_url": p.live_url,
            "url": reverse("core:project_detail", kwargs={"slug": p.slug}),
        }
        for p in Project.objects.all()
    ]
    return JsonResponse({"results": data})


def api_skills(request):
    data = [
        {"name": s.name, "category": s.category} for s in Skill.objects.all()
    ]
    return JsonResponse({"results": data})


def api_experience(request):
    data = [
        {
            "company": e.company,
            "role": e.role,
            "timeframe": e.timeframe,
            "technologies": e.technology_list,
        }
        for e in Experience.objects.all()
    ]
    return JsonResponse({"results": data})


@require_http_methods(["POST"])
def api_contact(request):
    payload = request.POST
    if not payload:
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "errors": {"__all__": ["Invalid JSON body."]}}, status=400)
    form = ContactForm(payload)
    if form.is_valid():
        form.save()
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
