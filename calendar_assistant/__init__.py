"""AI Calendar Assistant for Outlook and Google Calendar."""

__version__ = "0.1.0"

from .base import CalendarAssistant
from .google_calendar import GoogleCalendarAssistant
from .outlook_calendar import OutlookCalendarAssistant

__all__ = ["CalendarAssistant", "GoogleCalendarAssistant", "OutlookCalendarAssistant"]
