import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(name="apps.core.tasks.send_email_task", bind=True, max_retries=3, default_retry_delay=60)  # 🔥 explicit név!
def send_email_task(self, subject, recipient_email, context, template_name="emails/default.html", from_email=None):
    """
    Celery task to send an email with optional HTML template rendering.

    Parameters:
    - subject (str): Email subject line.
    - recipient_email (str): The recipient's email address.
    - context (dict): Context data for rendering the template.
    - template_name (str): Path to the HTML template (default: 'emails/default.html').
    - from_email (str, optional): Sender email address. Defaults to settings.DEFAULT_FROM_EMAIL.

    Fallbacks:
    - Sends a plain-text version if HTML fails.
    - Logs errors and retries on failure (max 3 times).
    """
    try:
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        html_content = render_to_string(template_name, context)
        text_content = render_to_string(template_name.replace(".html", ".txt"), context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        logger.info(f"✅ Email sent to {recipient_email} using template {template_name}")
    except Exception as e:
        logger.exception(f"❌ Failed to send email to {recipient_email}. Retrying...")
        raise self.retry(exc=e)
