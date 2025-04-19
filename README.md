# inter-hm

# Dev env

    docker-compose -f local.yml up

# Ha fejleszteni akarsz

Csinálj egy venvet

    python3 -m venv venv

Aktiváld

    source venv/bin/activate

Telepítsd a fejlesztői dependencyket

    pip install -r requirements/local.txt

Aktivált a pre-commitot

    pre-commit install
    pre-commit run

# core module

A core moduleban csak segéd osztályokat tárolunk pl crudcontroller, abstract modellek, alap permissioniok

- Ha crud endpointokra van szükséged használd a apps.core.crud_controller.CrudController segéd osztályt
- Ha olyan modelt csinálsz amibe eltárolod a usert aki csinálta használd a apps.core.models.HasOwner abstract modelt

# Subscriptions

Az előfizetési rendszer stripeot használ, pricing tableökkel és webhookokkal.

## Konfigurálás

https://dashboard.stripe.com/

### Csomagok létrehozása

A csomagokat a product catalogban kell létrehozni

### Csomagok konfigurálása

Minden terméknél bekell állítani Metadatának egy kulcs-érték párt,
ahol a kulcs az allowed_job_posts, az érték pedig az adott csomagnál,
hány hírdetést adhat fel az adott előfizető

### Pricing table

A product catalog oldalon a pricing tables fül alatt lehet létrehozni.

## Egyéb beállítások

### Webhook

A szoftver a /stripe/webhook/ végponton várja a stripe által küldött webhookokat. <br>
A stripe felületén így állítsd be https://your-domain.com/stripe/webhook/

### Multiple Subscriptions - kapcsold KI

https://dashboard.stripe.com/settings/checkout

https://docs.stripe.com/payments/checkout/limit-subscriptions

Nem engedjük, hogy egy felhasználónak több előfizetése legyen 1 időben

## Környezeti változók

| Megnevezés                 | Leírás                                                                                                                       |
|----------------------------|------------------------------------------------------------------------------------------------------------------------------|
| STRIPE_LIVE_SECRET_KEY     | https://docs.stripe.com/keys                                                                                                 |
| STRIPE_TEST_SECRET_KEY     | -                                                                                                                            |
| STRIPE_PRICING_TABLE_ID    | https://docs.stripe.com/no-code/pricing-table#Create                                                                         |
| STRIPE_PUBLIC_KEY          | https://stripe.com/login?redirect=/account/apikeys (Ha nem látod, kattints a Developers gombra majd az API keys almenüpotra) |
| STRIPE_CUSTOMER_PORTAL_URL | https://docs.stripe.com/no-code/pricing-table#customer-portal                                                                |
| DJSTRIPE_WEBHOOK_SECRET    | https://docs.stripe.com/webhooks#register-webhook                                                                            |

# Beállítások

## Környezeti változók

| **Megnevezés**             | **Leírás**                                                               | **Alapértelmezett** | **Példa**               |
|----------------------------|--------------------------------------------------------------------------|:--------------------|:------------------------|
| **DB**                     |                                                                          |                     |                         |
| POSTGRES_DB                |                                                                          |                     | inter_hm                |
| POSTGRES_USER              |                                                                          |                     | inter_hm                |
| POSTGRES_PASSWORD          |                                                                          |                     | SecretPassword          |
| POSTGRES_HOST              |                                                                          | postgres            | postgres                |
| POSTGRES_PORT              |                                                                          | 5432                | 5432                    |
| **Email**                  |                                                                          |                     |                         |
| DJANGO_EMAIL_USE_TLS       |                                                                          |                     | 1                       |
| DJANGO_EMAIL_HOST          |                                                                          |                     | smtp.gmail.com          |
| DJANGO_EMAIL_PORT          |                                                                          | 587                 | 587                     |
| DJANGO_EMAIL_HOST_USER     |                                                                          |                     | your_account@gmail.com  |
| DJANGO_EMAIL_HOST_PASSWORD |                                                                          |                     | your account’s password |
| **Egyéb**                  |                                                                          |                     |                         |
| DJANGO_SECRET_KEY          | Ezt használja a rendszer a bejelentkezési és egyéb adatok hitelesítésére |                     |                         |

### Secret Key generálás

Lehetőleg ne a szerveren legyen generálva, hogy ne kelljen le buildelni a fejlesztői imaget és containert

    docker-compose -f local.yml run --rm django python -c 'from django.core.management.utils import get_random_secret_key;print(get_random_secret_key())'
    docker-compose -f local.yml run --rm django python manage.py 
