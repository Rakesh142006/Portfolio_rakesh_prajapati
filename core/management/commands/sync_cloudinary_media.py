"""
Management command: sync_cloudinary_media

WHY THIS EXISTS
----------------
Your Project/Certificate/Profile image fields store plain relative paths
(e.g. "projects/babysitter.png") that were saved back when the files were
written straight to the local media/ folder. Your settings.py now has:

    DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

...so Django builds every image <img src> as a Cloudinary CDN URL from
that stored path. But the actual image bytes were NEVER uploaded to your
Cloudinary account - only the DB path exists. Result: broken images.

This command finds each record's local file on disk, and re-saves it
through the model field so cloudinary_storage actually uploads it and
rewrites the DB field to the real Cloudinary reference.

HOW TO USE
----------
1. Copy this file to: core/management/commands/sync_cloudinary_media.py
   (create the management/ and management/commands/ folders with empty
   __init__.py files if they don't already exist)
2. Make sure your .env / environment has valid CLOUDINARY_CLOUD_NAME,
   CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET (see steps below).
3. Run:  python manage.py sync_cloudinary_media
4. Check the Cloudinary Media Library dashboard - the files should now
   appear there, and your site's images should load.
"""
import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Project, Certificate, Profile


class Command(BaseCommand):
    help = "Re-upload existing local media/ files to Cloudinary and fix DB references."

    def handle(self, *args, **options):
        media_root = settings.MEDIA_ROOT or (settings.BASE_DIR / "media")

        def resync(instance, field_name):
            field = getattr(instance, field_name)
            if not field:
                return
            # field.name is the relative path stored in the DB, e.g. "projects/babysitter.png"
            local_path = os.path.join(media_root, field.name)
            if not os.path.exists(local_path):
                self.stdout.write(self.style.WARNING(
                    f"  SKIP {instance}: no local file at {local_path}"
                ))
                return
            with open(local_path, "rb") as f:
                django_file = File(f, name=os.path.basename(field.name))
                # save=True triggers the storage backend (Cloudinary) to actually upload it
                field.save(django_file.name, django_file, save=True)
            self.stdout.write(self.style.SUCCESS(f"  Uploaded {instance} -> {field.name}"))

        self.stdout.write("Syncing Project images...")
        for p in Project.objects.all():
            resync(p, "image")

        self.stdout.write("Syncing Certificate images...")
        for c in Certificate.objects.all():
            resync(c, "image")

        self.stdout.write("Syncing Profile image + resume...")
        profile = Profile.load()
        resync(profile, "profile_image")
        resync(profile, "resume")

        self.stdout.write(self.style.SUCCESS("Done. Check Cloudinary Media Library and your site."))