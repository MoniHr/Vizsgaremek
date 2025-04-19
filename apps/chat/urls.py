from django.urls import path
from apps.chat import views

urlpatterns = [
    path("", views.chat_view, name="chat"),  # Fő chat nézet, GET paraméterrel működik: ?room=<uuid>
    path("create/<int:user_id>/", views.create_chat, name="chat_create"),  # Új szoba létrehozása egy felhasználóval
    path("send/<uuid:room_id>/", views.send_message, name="chat_send_message"),  # Üzenetküldés
    path("mark-read/<uuid:room_id>/", views.mark_messages_read, name="chat_mark_read"),  # Olvasottra állítás
    path("unread-count/", views.unread_messages_count, name="chat_unread_count"),  # Összes olvasatlan számláló
]

