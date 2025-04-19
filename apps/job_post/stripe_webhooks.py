from django.utils import timezone
from datetime import timedelta, datetime, timezone as dt_timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from apps.job_post.models import JobPost
import stripe


# TODO: EMail küldés

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return HttpResponseBadRequest(f"Webhook error: {str(e)}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})
        customer_details = session.get("customer_details", {})
        address = customer_details.get("address", {})

        job_post_id = metadata.get("job_post_id")
        plan_id = metadata.get("plan_id")

        if job_post_id:
            try:
                job = JobPost.objects.get(pk=job_post_id)
                now = timezone.now()

                # 🔥 Boost aktiválás
                job.is_boosted = True
                job.boost_start_date = now
                job.boost_end_date = now + timedelta(days=30)
                job.title_editable_until = now + timedelta(days=5)

                # 🧾 Plan hozzárendelés
                if plan_id:
                    from apps.job_post.models import JobPlan
                    plan = JobPlan.objects.filter(pk=plan_id).first()
                    if plan:
                        job.selected_plan = plan
                        job.boost_end_date = now + timedelta(days=plan.duration_days)
                        job.boost_location = plan.plan_type

                # 📦 Billing adatok Stripe-ból
                job.billing_name = customer_details.get("name")
                job.billing_address = address.get("line1")
                job.billing_city = address.get("city")
                job.billing_state = address.get("state")
                job.billing_zip_code = address.get("postal_code")
                job.billing_country = address.get("country")

                # 💳 Stripe tranzakciós adatok mentése
                job.stripe_checkout_session_id = session.get("id")
                job.stripe_payment_intent_id = session.get("payment_intent")
                job.stripe_customer_email = customer_details.get("email")

                # ⏱ Stripe esemény időpontja (UNIX timestamp → datetime)
                event_timestamp = event.get("created")
                if event_timestamp:
                    job.stripe_transaction_completed_at = datetime.fromtimestamp(event_timestamp, tz=dt_timezone.utc)

                job.save()
                return HttpResponse(status=200)

            except JobPost.DoesNotExist:
                return HttpResponse(status=404)

    return HttpResponse(status=200)
