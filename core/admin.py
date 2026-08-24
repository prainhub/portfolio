from django.contrib import admin, messages

from .models import (
    Certification,
    ContactMessage,
    CurrentlyLearning,
    Education,
    Experience,
    Profile,
    Project,
    ProjectFeature,
    ProjectScreenshot,
    Skill,
    SocialLink,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "headline", "email")

    def has_add_permission(self, request):
        # Keep this a singleton — edit the existing row instead of adding more.
        return not Profile.objects.exists()


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "label", "url", "order")
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "timeframe", "order")
    list_editable = ("order",)
    search_fields = ("role", "company")


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "timeframe", "order", "created_at")
    list_editable = ("featured", "order")
    list_filter = ("category", "featured")
    search_fields = ("title", "technologies", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectFeatureInline, ProjectScreenshotInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "category", "timeframe", "featured", "order")}),
        ("Summary", {"fields": ("short_description", "technologies", "image")}),
        ("Links", {"fields": ("github_url", "live_url")}),
        (
            "Project detail page",
            {
                "fields": (
                    "problem_statement",
                    "solution",
                    "architecture_notes",
                    "challenges",
                    "future_improvements",
                )
            },
        ),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_editable = ("order",)
    list_filter = ("category",)
    ordering = ("category", "order")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "year_range", "grade", "order")
    list_editable = ("order",)


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "issue_date", "order")
    list_editable = ("order",)


@admin.register(CurrentlyLearning)
class CurrentlyLearningAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    actions = ["mark_as_read", "mark_as_unread"]

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} message(s) marked as read.", messages.SUCCESS)

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} message(s) marked as unread.", messages.SUCCESS)


admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage your portfolio content"
