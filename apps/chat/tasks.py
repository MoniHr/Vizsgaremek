import json
import logging
from apps.chat.models import ChatMessage, ChatRoom
from apps.chat.utils import publish_unread_count  # 👈 Hozzáadva
from celery import shared_task
from django.utils.timezone import now
from django.contrib.auth import get_user_model
import redis

logger = logging.getLogger(__name__)
User = get_user_model()
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@shared_task(bind=True)
def save_chat_message(self, chat_room_id, sender_email, message):
    """ Celery task az üzenetek mentésére és WebSocket továbbítására. """

    logger.info(f"✅ Celery task indítva! Room ID: {chat_room_id}, Sender: {sender_email}")

    try:
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        sender = User.objects.get(email=sender_email)
        receiver = chat_room.user1 if sender == chat_room.user2 else chat_room.user2

        new_message = ChatMessage.objects.create(
            chat_room=chat_room,
            sender=sender,
            receiver=receiver,
            message=message
        )

        # 🔄 ChatRoom update
        chat_room.last_message = message
        chat_room.last_message_time = now()
        chat_room.save(update_fields=["last_message", "last_message_time"])

        logger.info(f"✅ Üzenet mentve! Message ID: {new_message.id}")

        # 🔥 WebSocket message - chat
        message_data = {
            "chat_room": str(chat_room.id),
            "sender": sender_email,
            "receiver": receiver.email,
            "message": message,
            "timestamp": new_message.timestamp.strftime("%Y-%m-%d %H:%M"),
        }
        redis_client.publish("chat_messages", json.dumps(message_data))

        # ✅ 🔔 WebSocket message - új olvasatlan üzenetszám
        unread_count = ChatMessage.objects.filter(receiver=receiver, is_read=False).count()
        publish_unread_count(receiver.email, unread_count)

        return {"status": "success", "message_id": new_message.id}

    except ChatRoom.DoesNotExist:
        logger.error(f"❌ Chat room nem található! Room ID: {chat_room_id}")
        self.retry(countdown=5, max_retries=3)
        return {"status": "error", "message": "Chat room not found"}

    except User.DoesNotExist:
        logger.error(f"❌ Felhasználó nem található! Email: {sender_email}")
        return {"status": "error", "message": "User not found"}

    except Exception as e:
        logger.exception(f"❌ Hiba történt az üzenet mentése közben! Room ID: {chat_room_id}")
        return {"status": "error", "message": str(e)}
