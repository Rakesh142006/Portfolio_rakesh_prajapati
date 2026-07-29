from django.contrib import admin
from .models import Skill, Project, Certificate, ContactMessage, Profile, Experience


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "order")
    list_editable = ("proficiency", "order")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "created_at", "order")
    list_editable = ("featured", "order")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description", "tech_stack")
    list_filter = ("featured",)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "issue_date", "order")
    list_editable = ("order",)
    search_fields = ("title", "issuer")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "start_date", "end_date", "is_current", "order")
    list_editable = ("order",)
    list_filter = ("is_current",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "tagline", "email")

    def has_add_permission(self, request):
        return not Profile.objects.exists()
