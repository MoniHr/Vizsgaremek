from django.contrib import admin
from .models import ChatRoom, ChatMessage

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "user1", "user2", "last_message", "last_message_time", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user1__email", "user2__email", "last_message")
    ordering = ("-last_message_time",)

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("chat_room", "sender", "receiver", "message_preview", "timestamp", "is_read")
    list_filter = ("is_read", "timestamp")
    search_fields = ("sender__email", "receiver__email", "message")
    ordering = ("-timestamp",)

    def message_preview(self, obj):
        return obj.message[:50] + ("..." if len(obj.message) > 50 else "")
    message_preview.short_description = "Message Preview"

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True
