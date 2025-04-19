# apps/chat/utils.py
import json
import redis

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

def publish_unread_count(user_email, count):
    data = {
        "user": user_email,
        "unread_count": count,
    }
    redis_client.publish("chat_unread_count", json.dumps(data))
