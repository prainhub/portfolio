from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("contact/", views.contact, name="contact"),
    path("resume/", views.resume_view, name="resume_view"),
    path("resume/download/", views.resume_download, name="resume_download"),
    path("api/projects/", views.api_projects, name="api_projects"),
    path("api/skills/", views.api_skills, name="api_skills"),
    path("api/experience/", views.api_experience, name="api_experience"),
    path("api/contact/", views.api_contact, name="api_contact"),
]
