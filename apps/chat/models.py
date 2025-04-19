import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxLengthValidator

User = get_user_model()


class ChatRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatrooms_as_user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatrooms_as_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    last_message = models.TextField(null=True, blank=True)
    last_message_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user1", "user2"], name="unique_private_chat")
        ]

        indexes = [
            models.Index(fields=["last_message_time"]),
        ]

    def __str__(self):
        return f"ChatRoom: {self.user1} ↔ {self.user2}"

    def has_access(self, user):
        return user in [self.user1, self.user2]

    def unread_messages_count(self, user):
        return self.messages.filter(receiver=user, is_read=False).count()

    @staticmethod
    def get_or_create_private_chat(user1, user2):
        if user1 == user2:
            raise ValueError("Cannot create a chat with yourself.")
        user1, user2 = sorted([user1, user2], key=lambda u: u.id)
        return ChatRoom.objects.get_or_create(user1=user1, user2=user2)


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    message = models.TextField(validators=[MaxLengthValidator(500)])
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["timestamp"]
        indexes = [
            models.Index(fields=["chat_room", "timestamp"]),
            models.Index(fields=["receiver", "is_read"]),
            models.Index(fields=["sender"]),
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.message[:30]}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Direkt SQL update gyorsabb, nem kell új save()
            ChatRoom.objects.filter(id=self.chat_room.id).update(
                last_message=self.message,
                last_message_time=self.timestamp
            )
