from django.core.validators import MinLengthValidator
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    """
    Singleton-style row holding the top-level identity/summary content.
    Editable in the admin — create/keep exactly one row.
    """

    full_name = models.CharField(max_length=120)
    headline = models.CharField(
        max_length=160, help_text="e.g. Python Developer | Junior AI Engineer"
    )
    tagline = models.CharField(
        max_length=220,
        help_text="One-line statement of what you build, shown in the hero.",
    )
    summary = models.TextField(help_text="About-section narrative.")
    looking_for = models.CharField(
        max_length=255,
        blank=True,
        help_text="Type of role/opportunity you're seeking.",
    )
    location = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ("github", "GitHub"),
        ("linkedin", "LinkedIn"),
        ("email", "Email"),
        ("phone", "Phone"),
        ("twitter", "X / Twitter"),
        ("website", "Website"),
        ("other", "Other"),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    label = models.CharField(max_length=60, blank=True)
    url = models.CharField(
        max_length=300,
        help_text="Full URL, or mailto:/tel: for email and phone.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "platform"]

    def __str__(self):
        return self.label or self.get_platform_display()


class Experience(models.Model):
    company = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    location = models.CharField(max_length=120, blank=True)
    timeframe = models.CharField(
        max_length=60, help_text='e.g. "Mar 2025" or "Jun – Jul 2025"'
    )
    description = models.TextField(
        help_text="One responsibility/contribution per line."
    )
    technologies = models.CharField(
        max_length=300, blank=True, help_text="Comma-separated."
    )
    company_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return f"{self.role} — {self.company}"

    @property
    def description_lines(self):
        return [line.strip() for line in self.description.splitlines() if line.strip()]

    @property
    def technology_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("ai", "AI"),
        ("fullstack", "Full Stack"),
        ("web", "Web"),
        ("ml", "Machine Learning"),
        ("other", "Other"),
    ]

    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    timeframe = models.CharField(max_length=60, blank=True, help_text='e.g. "Feb 2026"')
    short_description = models.CharField(
        max_length=220, help_text="One or two sentences, shown on the project card."
    )
    problem_statement = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    architecture_notes = models.TextField(
        blank=True,
        help_text="One pipeline stage per line, e.g. 'Frontend → Django → ...'.",
    )
    challenges = models.TextField(blank=True)
    future_improvements = models.TextField(blank=True)
    technologies = models.CharField(max_length=400, help_text="Comma-separated.")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="web")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-featured", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:project_detail", kwargs={"slug": self.slug})

    @property
    def technology_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]

    @property
    def architecture_steps(self):
        return [
            line.strip() for line in self.architecture_notes.splitlines() if line.strip()
        ]

    @property
    def challenge_lines(self):
        return [line.strip() for line in self.challenges.splitlines() if line.strip()]


class ProjectFeature(models.Model):
    project = models.ForeignKey(Project, related_name="features", on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(
        Project, related_name="screenshots", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="projects/screenshots/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Screenshot for {self.project}"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("ai_ml", "AI / ML"),
        ("backend", "Backend"),
        ("frontend", "Frontend"),
        ("database", "Database"),
        ("cloud", "Cloud & Deploy"),
        ("tools", "Tools"),
        ("soft", "Soft Skills"),
    ]

    name = models.CharField(max_length=80)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(
        max_length=10,
        blank=True,
        help_text="Optional short glyph/initials shown on the skill chip.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category", "order", "name"]

    def __str__(self):
        return self.name


class Education(models.Model):
    institution = models.CharField(max_length=160)
    degree = models.CharField(max_length=160)
    field = models.CharField(max_length=160, blank=True)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(null=True, blank=True)
    grade = models.CharField(max_length=60, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_year"]

    def __str__(self):
        return f"{self.degree} — {self.institution}"

    @property
    def year_range(self):
        if self.end_year:
            return f"{self.start_year} – {self.end_year}"
        return f"{self.start_year} – Present"


class Certification(models.Model):
    name = models.CharField(max_length=160)
    organization = models.CharField(max_length=160)
    issue_date = models.CharField(max_length=40, help_text='e.g. "Jan 2025" or "2025"')
    credential_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.name


class CurrentlyLearning(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=220)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "Currently learning"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=160)
    message = models.TextField(validators=[MinLengthValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} — {self.name}"
