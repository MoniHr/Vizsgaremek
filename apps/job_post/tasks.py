from celery import shared_task
from .models import JobPost

# TODO: elelnörzés kell még és kész is van.
# Kell még egy jelző hogy mar csak 5 nap van vissza és emailt is kóldjün ki..
# Tablazatot kell kiirni még.. a tablzat neveket...

@shared_task
def send_expiration_reminders():
    jobs = JobPost.objects.filter(
        is_boosted=True,
        expiration_reminder_sent=False,
        boost_end_date__isnull=False
    )

    for job in jobs:
        if job.should_send_expiration_reminder():
            # TODO: email küldés
            # pl. küldj emailt (send_mail...)
            print(f"🟡 Reminder: '{job.title}' hamarosan lejár.")
            job.expiration_reminder_sent = True
            job.save()


