# Django Portfolio Website

A personal portfolio website built with Django. It showcases skills, projects, certificates, and work experience, and includes a working contact form that emails you directly. All content — profile info, skills, projects, certificates, and experience — is fully editable through the Django admin, so no code changes are needed to update the site.

## Features

- **Home page** — highlights featured projects, top skills, and recent certificates
- **About page** — bio, categorized skills (language, framework, database, tool, other), and a full work experience timeline
- **Projects** — list and detail views for each project, with tech stack, GitHub/live links, and auto-generated slugs
- **Certificates** — list of certifications with issuer, date, and credential links
- **Contact form** — validated form that saves messages to the database and emails the site owner, with a reply-to set to the sender
- **Global profile context** — the site owner's profile is available in every template via a custom context processor
- **Admin-managed content** — everything (profile, skills, projects, certificates, experience, messages) is editable from the Django admin, with `Profile` implemented as a singleton so there's only ever one owner record

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (default) / any Django-supported DB
- **Email:** Django's `EmailMessage` (SMTP backend recommended for production)
- **Frontend:** Django templates (HTML/CSS)

## Project Structure

```
core/
├── apps.py                 # App configuration
├── context_processors.py   # Injects `profile` into every template
├── forms.py                 # ContactForm (ModelForm)
├── models.py                # Skill, Project, Certificate, ContactMessage, Profile, Experience
├── urls.py                  # App URL routes
├── views.py                  # Home, About, Projects, Certificates, Contact views
├── tests.py
├── templates/core/          # HTML templates (home, about, projects, project_detail, certificates, contact)
└── migrations/
```

## Models

| Model | Purpose |
|---|---|
| `Profile` | Singleton record with your name, tagline, bio, contact info, social links, resume, and profile image |
| `Skill` | Individual skills with category and proficiency (0–100) |
| `Project` | Portfolio projects with description, tech stack, images, and links |
| `Certificate` | Certifications with issuer, date, and credential URL |
| `Experience` | Work history entries with role, company, dates, and bullet-point descriptions |
| `ContactMessage` | Messages submitted through the contact form |

## Getting Started

### Prerequisites

- Python 3.10+
- pip / virtualenv

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create a superuser to access the admin
python manage.py createsuperuser

# Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/` to manage content.

### Environment Variables

Set the following in your `.env` or settings file for the contact form to work:

```
DEFAULT_FROM_EMAIL=your-from-address@example.com
CONTACT_RECEIVER_EMAIL=your-inbox@example.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-smtp-username
EMAIL_HOST_PASSWORD=your-smtp-password
```

## Usage

1. Log in to `/admin/` and fill out your **Profile** (name, tagline, bio, links, resume, photo).
2. Add your **Skills**, marking category and proficiency.
3. Add **Projects**, marking key ones as `featured` so they show on the home page.
4. Add **Certificates** and **Experience** entries.
5. Messages submitted through the **Contact** page appear in the admin under `Contact Messages` and are emailed to you.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

Built by [Your Name] — feel free to reach out via the contact form on the live site or through the links in the profile section.