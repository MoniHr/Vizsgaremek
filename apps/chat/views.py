import json
from apps.chat.models import ChatMessage, ChatRoom
import redis
import logging
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib import messages
from apps.chat.tasks import save_chat_message

User = get_user_model()
logger = logging.getLogger(__name__)
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True)


@login_required
@never_cache
def chat_view(request):
    chat_room_id = request.GET.get("room")
    selected_room = None
    chat_messages = []
    other_user = None

    chat_rooms_qs = ChatRoom.objects.filter(
        Q(user1=request.user) | Q(user2=request.user)
    ).exclude(user1=request.user, user2=request.user)  # 🚫 Saját magaddal való szoba kizárása
    chat_rooms_qs = chat_rooms_qs.order_by("-last_message_time")

    chat_rooms = []
    for room in chat_rooms_qs:
        other = room.user2 if room.user1 == request.user else room.user1
        unread_count = room.messages.filter(receiver=request.user, is_read=False).count()

        chat_rooms.append({
            "id": room.id,
            "last_message_time": room.last_message_time,
            "last_message": room.last_message,
            "unread_count": unread_count,
            "other_user": other,
        })

    if chat_room_id:
        try:
            selected_room = ChatRoom.objects.get(id=chat_room_id)

            # 🔒 Hozzáférés-ellenőrzés
            if not selected_room.has_access(request.user):
                return JsonResponse({'error': 'Unauthorized'}, status=403)

            # 🔄 Üzenetek betöltése és olvasottra állítás
            chat_messages = selected_room.messages.order_by("timestamp")
            other_user = selected_room.user2 if selected_room.user1 == request.user else selected_room.user1

            updated_count = selected_room.messages.filter(receiver=request.user, is_read=False).update(is_read=True)
            if updated_count > 0:
                redis_client.publish("chat_read_receipts", json.dumps({
                    "chat_room": str(selected_room.id),
                    "user": request.user.email,
                    "updated_messages": updated_count
                }))
        except ChatRoom.DoesNotExist:
            selected_room = None

    return render(request, "chat/chat.html", {
        "chat_rooms": chat_rooms,
        "chat_room": selected_room,
        "chat_messages": chat_messages,
        "other_user": other_user
    })

@login_required
def create_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    if other_user == request.user:
        messages.error(request, "You cannot start a chat with yourself.")
        return redirect("chat")

    chat_room = ChatRoom.objects.filter(
        Q(user1=request.user, user2=other_user) | Q(user1=other_user, user2=request.user)
    ).first()

    if chat_room:
        return redirect(f"{settings.CHAT_BASE_URL}?room={chat_room.id}")

    chat_room = ChatRoom.objects.create(user1=request.user, user2=other_user)
    return redirect(f"{settings.CHAT_BASE_URL}?room={chat_room.id}")


@csrf_exempt
@login_required
def send_message(request, room_id):
    logger.info(f"📨 Új üzenet fogadva! Room ID: {room_id}, Feladó: {request.user.email}")

    chat_room = get_object_or_404(ChatRoom, id=room_id)

    if not chat_room.has_access(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        message = data.get("message")

        if not message:
            return JsonResponse({'error': 'Message content required'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)

    try:
        task_result = save_chat_message.delay(str(chat_room.id), request.user.email, message)
        return JsonResponse({
            "status": "success",
            "task_id": task_result.id,
            "message": "Message processing (Celery)"
        })
    except Exception as e:
        logger.exception("❌ Celery hiba!")
        return JsonResponse({'error': 'Internal server error', 'details': str(e)}, status=500)


@login_required
def mark_messages_read(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)

    if not chat_room.has_access(request.user):
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    updated_count = chat_room.messages.filter(receiver=request.user, is_read=False).update(is_read=True)

    redis_client.publish("chat_read_receipts", json.dumps({
        "chat_room": str(chat_room.id),
        "user": request.user.email,
        "updated_messages": updated_count
    }))

    return JsonResponse({"updated_messages": updated_count})


@login_required
def unread_messages_count(request):
    unread_count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({"unread_count": unread_count})
