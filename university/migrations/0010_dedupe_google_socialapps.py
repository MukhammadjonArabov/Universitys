from django.db import migrations


def dedupe_google_socialapps(apps, schema_editor):
    Site = apps.get_model("sites", "Site")
    SocialApp = apps.get_model("socialaccount", "SocialApp")
    from django.conf import settings

    site, _ = Site.objects.get_or_create(
        pk=settings.SITE_ID,
        defaults={
            "domain": getattr(settings, "SITE_DOMAIN", "localhost:8000"),
            "name": getattr(settings, "SITE_NAME", "Universitys Local"),
        },
    )

    google_apps = list(SocialApp.objects.filter(provider="google").order_by("id"))
    if google_apps:
        app = google_apps[0]
    else:
        app = SocialApp(provider="google", name="Google", key="")

    app.name = "Google"
    app.client_id = getattr(settings, "GOOGLE_CLIENT_ID", "") or app.client_id
    app.secret = getattr(settings, "GOOGLE_CLIENT_SECRET", "") or app.secret
    app.key = ""
    app.save()
    app.sites.set([site])

    duplicate_ids = [item.id for item in google_apps[1:]]
    if duplicate_ids:
        SocialApp.objects.filter(id__in=duplicate_ids).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("university", "0009_create_google_socialapp_and_update_site"),
        ("sites", "0001_initial"),
        ("socialaccount", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(dedupe_google_socialapps, reverse_code=migrations.RunPython.noop),
    ]
