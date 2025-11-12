"""Google Calendar integration."""

import os
import pickle
from datetime import datetime, timedelta
from typing import List, Dict, Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from .base import CalendarAssistant


class GoogleCalendarAssistant(CalendarAssistant):
    """Google Calendar assistant implementation."""

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, credentials_path: str = 'credentials.json', token_path: str = 'token.pickle'):
        """Initialize Google Calendar assistant.
        
        Args:
            credentials_path: Path to Google OAuth credentials file
            token_path: Path to store authentication token
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.service = None
        self.creds = None

    def authenticate(self) -> bool:
        """Authenticate with Google Calendar API.
        
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        try:
            # Load existing token if available
            if os.path.exists(self.token_path):
                with open(self.token_path, 'rb') as token:
                    self.creds = pickle.load(token)

            # Refresh or create new credentials if needed
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    if not os.path.exists(self.credentials_path):
                        print(f"Credentials file not found: {self.credentials_path}")
                        return False
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, self.SCOPES
                    )
                    self.creds = flow.run_local_server(port=0)

                # Save credentials for next run
                with open(self.token_path, 'wb') as token:
                    pickle.dump(self.creds, token)

            self.service = build('calendar', 'v3', credentials=self.creds)
            return True

        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def list_events(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        max_results: int = 10
    ) -> List[Dict]:
        """List calendar events within a time range.
        
        Args:
            start_time: Start of time range (default: now)
            end_time: End of time range (default: 7 days from now)
            max_results: Maximum number of events to return
            
        Returns:
            List of event dictionaries
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        if start_time is None:
            start_time = datetime.utcnow()
        if end_time is None:
            end_time = start_time + timedelta(days=7)

        events_result = self.service.events().list(
            calendarId='primary',
            timeMin=start_time.isoformat() + 'Z',
            timeMax=end_time.isoformat() + 'Z',
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])

    def create_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        description: Optional[str] = None,
        location: Optional[str] = None,
        attendees: Optional[List[str]] = None
    ) -> Dict:
        """Create a new calendar event.
        
        Args:
            summary: Event title/summary
            start_time: Event start time
            end_time: Event end time
            description: Event description (optional)
            location: Event location (optional)
            attendees: List of attendee email addresses (optional)
            
        Returns:
            Created event dictionary
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        event = {
            'summary': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
        }

        if description:
            event['description'] = description
        if location:
            event['location'] = location
        if attendees:
            event['attendees'] = [{'email': email} for email in attendees]

        created_event = self.service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        return created_event

    def update_event(
        self,
        event_id: str,
        summary: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        description: Optional[str] = None,
        location: Optional[str] = None
    ) -> Dict:
        """Update an existing calendar event.
        
        Args:
            event_id: ID of the event to update
            summary: New event title/summary (optional)
            start_time: New event start time (optional)
            end_time: New event end time (optional)
            description: New event description (optional)
            location: New event location (optional)
            
        Returns:
            Updated event dictionary
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        # Get the existing event
        event = self.service.events().get(
            calendarId='primary',
            eventId=event_id
        ).execute()

        # Update fields
        if summary:
            event['summary'] = summary
        if start_time:
            event['start'] = {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            }
        if end_time:
            event['end'] = {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            }
        if description:
            event['description'] = description
        if location:
            event['location'] = location

        updated_event = self.service.events().update(
            calendarId='primary',
            eventId=event_id,
            body=event
        ).execute()

        return updated_event

    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event.
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            bool: True if deletion successful, False otherwise.
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=event_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error deleting event: {e}")
            return False

    def search_events(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search for calendar events by query string.
        
        Args:
            query: Search query string
            max_results: Maximum number of events to return
            
        Returns:
            List of matching event dictionaries
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        events_result = self.service.events().list(
            calendarId='primary',
            q=query,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        return events_result.get('items', [])
