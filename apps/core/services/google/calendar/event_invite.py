from dataclasses import dataclass
from datetime import datetime


@dataclass
class EventInvite:
    event_title: str
    attendees: list[str]
    start_date: datetime
    end_date: datetime
    event_description: str = ""
    send_notifications: bool = False
    visibility: str = "public"
