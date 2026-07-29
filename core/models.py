from django.db import models
from django.utils import timezone


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("language", "Language"),
        ("framework", "Framework / Library"),
        ("database", "Database"),
        ("tool", "Tool / Platform"),
        ("other", "Other"),
    ]
    name = models.CharField(max_length=60)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="other")
    proficiency = models.PositiveIntegerField(default=70, help_text="0-100")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    summary = models.CharField(max_length=220, help_text="Short one-line summary shown on cards")
    description = models.TextField()
    tech_stack = models.CharField(max_length=200, help_text="Comma-separated, e.g. Django, PostgreSQL, HTMX")
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(",") if t.strip()]

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base = slugify(self.title)
            slug = base
            i = 1
            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)


class Certificate(models.Model):
    title = models.CharField(max_length=150)
    issuer = models.CharField(max_length=150)
    issue_date = models.DateField()
    credential_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="certificates/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-issue_date"]

    def __str__(self):
        return f"{self.title} — {self.issuer}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.subject or 'No subject'}"


class Profile(models.Model):
    """Singleton-style model holding the site owner's info, editable from admin."""
    full_name = models.CharField(max_length=120, default="Your Name")
    tagline = models.CharField(max_length=200, default="Backend Developer & Django Engineer")
    bio = models.TextField(default="Write a short bio about yourself here.")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=120, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    education = models.CharField(max_length=220, blank=True)
    resume = models.FileField(upload_to="resume/", blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile/", blank=True, null=True)
    years_experience = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Experience(models.Model):
    role = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(help_text="One point per line — rendered as a bullet list")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} @ {self.company}"

    def points(self):
        return [line.strip() for line in self.description.splitlines() if line.strip()]
