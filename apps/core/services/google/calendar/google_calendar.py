import random
import string
from datetime import datetime

import pytz
from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build

from apps.core.services.google.calendar.event_invite import EventInvite

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]


class GoogleCalendar:
    def __init__(self):
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        SERVICE_ACCOUNT_FILE = "credentials.json"

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        credentials = credentials.with_subject(settings.GOOGLE_CALENDAR)

        self.service = build("calendar", "v3", credentials=credentials)
        self.calendar_id = "primary"

    def get_upcoming_events(self, limit=10):
        now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

        events_result = (
            self.service.events()
            .list(
                calendarId=self.calendar_id,
                timeMin=now,
                maxResults=limit,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events

    @staticmethod
    def __date_to_utc(date):
        return (
            pytz.timezone(settings.TIME_ZONE)
            .localize(date.replace(tzinfo=None))
            .strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        )

    @staticmethod
    def __generate_random_string(length: int):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        result_str = "".join(random.choice(letters) for i in range(length))
        return result_str

    # https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.events.html#insert
    # insert(calendarId, body=None, conferenceDataVersion=None, maxAttendees=None, sendNotifications=None,
    # sendUpdates=None, supportsAttachments=None)
    def create_event(self, invite: EventInvite) -> dict:
        event = {
            "summary": invite.event_title,
            "kind": "calendar#event",
            "location": "",
            "description": invite.event_description,
            "start": {
                "dateTime": self.__date_to_utc(invite.start_date),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": self.__date_to_utc(invite.end_date),
                "timeZone": "UTC",
            },
            "conferenceData": {
                "createRequest": {
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                    "requestId": self.__generate_random_string(32),
                }
            },
            "attendees": [{"email": f} for f in invite.attendees],
            "visibility": invite.visibility,
            "sendNotifications": invite.send_notifications,
            "reminders": {
                "useDefault": True,
            },
        }

        insert_result = (
            self.service.events()
            .insert(calendarId=self.calendar_id, body=event, conferenceDataVersion=1)
            .execute()
        )
        return insert_result

    # https://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.events.html#delete
    # delete(calendarId, eventId, sendNotifications=None, sendUpdates=None)
    def delete_event(self, event_id: str) -> None:
        self.service.events().delete(
            calendarId=self.calendar_id, eventId=event_id, sendUpdates="all"
        ).execute()

    def update_event(self, event_id: str, invite: EventInvite) -> None:
        event = {
            "summary": invite.event_title,
            "kind": "calendar#event",
            "location": "",
            "description": invite.event_description,
            "start": {
                "dateTime": self.__date_to_utc(invite.start_date),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": self.__date_to_utc(invite.end_date),
                "timeZone": "UTC",
            },
            "attendees": [{"email": f} for f in invite.attendees],
            "visibility": invite.visibility,
            "sendNotifications": invite.send_notifications,
            "reminders": {
                "useDefault": True,
            },
        }
        self.service.events().patch(
            calendarId=self.calendar_id, eventId=event_id, body=event
        ).execute()
