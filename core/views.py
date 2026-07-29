from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ContactForm
from .models import Project, Certificate, Skill, Profile, Experience
from django.conf import settings
from django.core.mail import EmailMessage, BadHeaderError


def home(request):
    profile = Profile.load()
    featured_projects = Project.objects.filter(featured=True)[:3]
    skills = Skill.objects.all()
    certificates = Certificate.objects.all()[:3]
    context = {
        "profile": profile,
        "featured_projects": featured_projects,
        "skills": skills,
        "certificates": certificates,
        "project_count": Project.objects.count(),
        "certificate_count": Certificate.objects.count(),
    }
    return render(request, "core/home.html", context)


def about(request):
    profile = Profile.load()
    skills = Skill.objects.all()
    grouped_skills = {}
    for s in skills:
        grouped_skills.setdefault(s.get_category_display(), []).append(s)
    experiences = Experience.objects.all()
    context = {"profile": profile, "grouped_skills": grouped_skills, "experiences": experiences}
    return render(request, "core/about.html", context)


def project_list(request):
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "core/projects.html", context)


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    related = Project.objects.exclude(pk=project.pk)[:3]
    context = {"project": project, "related": related}
    return render(request, "core/project_detail.html", context)


def certificate_list(request):
    certificates = Certificate.objects.all()
    context = {"certificates": certificates}
    return render(request, "core/certificates.html", context)


def contact(request):
    profile = Profile.load()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()

            subject = f"New portfolio message: {contact_message.subject or 'No subject'}"
            body = (
                f"You've received a new message from your portfolio contact form.\n\n"
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {contact_message.subject or '(no subject)'}\n\n"
                f"Message:\n{contact_message.message}"
            )
            try:
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.CONTACT_RECEIVER_EMAIL],
                    reply_to=[contact_message.email],
                )
                email.send(fail_silently=False)
            except BadHeaderError:
                pass
            except Exception as e:
                print(f"Email send failed: {e}")

            messages.success(
                request,
                "Thanks for reaching out! Your message has been sent — I'll get back to you soon.",
            )
            return redirect("core:contact")
    else:
        form = ContactForm()
    context = {"form": form, "profile": profile}
    return render(request, "core/contact.html", context)
