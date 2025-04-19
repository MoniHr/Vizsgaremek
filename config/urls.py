from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from apps.accounts.views import register
from apps.job_post.stripe_webhooks import stripe_webhook_view
from apps.job_post.views import stripe_cancel, stripe_checkout_start, stripe_success

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.profile.urls")),
    path("search/", include("apps.search.urls")),
    path("jobs/", include("apps.job_post.urls")),
    path("chat/", include("apps.chat.urls")),
    path("", include("apps.pages.urls")),

    path("webhook/", stripe_webhook_view, name="stripe_webhook"),
    path("stripe/checkout/", stripe_checkout_start, name="stripe_checkout_start"),
    path("stripe/success/", stripe_success, name="stripe_success"),
    path("stripe/cancel/", stripe_cancel, name="stripe_cancel"),

    # Auth
    path("register/", register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm"),
    path("password_reset_complete/",auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),name="password_reset_complete"),
]

# Debug Toolbar (Csak ha telepítve van)
if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# Statikus és médiafájlok (fejlesztői mód)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
