"""Outlook Calendar integration."""

import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import msal
import requests

from .base import CalendarAssistant


class OutlookCalendarAssistant(CalendarAssistant):
    """Outlook Calendar assistant implementation."""

    SCOPES = ['Calendars.ReadWrite']
    AUTHORITY = 'https://login.microsoftonline.com/common'
    GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

    def __init__(self, client_id: str = None, client_secret: str = None, token_cache_path: str = 'outlook_token.json'):
        """Initialize Outlook Calendar assistant.
        
        Args:
            client_id: Azure AD application client ID
            client_secret: Azure AD application client secret (optional, for confidential client)
            token_cache_path: Path to store authentication token cache
        """
        self.client_id = client_id or os.getenv('OUTLOOK_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('OUTLOOK_CLIENT_SECRET')
        self.token_cache_path = token_cache_path
        self.access_token = None
        self.msal_app = None

        if not self.client_id:
            raise ValueError("Outlook client_id is required")

    def authenticate(self) -> bool:
        """Authenticate with Microsoft Graph API.
        
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        try:
            # Initialize MSAL application
            cache = msal.SerializableTokenCache()
            
            # Load token cache if exists
            if os.path.exists(self.token_cache_path):
                with open(self.token_cache_path, 'r') as f:
                    cache.deserialize(f.read())

            if self.client_secret:
                # Confidential client flow
                self.msal_app = msal.ConfidentialClientApplication(
                    self.client_id,
                    authority=self.AUTHORITY,
                    client_credential=self.client_secret,
                    token_cache=cache
                )
            else:
                # Public client flow
                self.msal_app = msal.PublicClientApplication(
                    self.client_id,
                    authority=self.AUTHORITY,
                    token_cache=cache
                )

            # Try to get token from cache
            accounts = self.msal_app.get_accounts()
            if accounts:
                result = self.msal_app.acquire_token_silent(
                    self.SCOPES,
                    account=accounts[0]
                )
                if result and 'access_token' in result:
                    self.access_token = result['access_token']
                    return True

            # Interactive authentication
            result = self.msal_app.acquire_token_interactive(
                scopes=self.SCOPES
            )

            if 'access_token' in result:
                self.access_token = result['access_token']
                
                # Save token cache
                with open(self.token_cache_path, 'w') as f:
                    f.write(cache.serialize())
                
                return True
            else:
                print(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
                return False

        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers with authentication token."""
        if not self.access_token:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

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
        if start_time is None:
            start_time = datetime.utcnow()
        if end_time is None:
            end_time = start_time + timedelta(days=7)

        url = f"{self.GRAPH_API_ENDPOINT}/me/calendarview"
        params = {
            'startDateTime': start_time.isoformat() + 'Z',
            'endDateTime': end_time.isoformat() + 'Z',
            '$top': max_results,
            '$orderby': 'start/dateTime'
        }

        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()

        return response.json().get('value', [])

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
        url = f"{self.GRAPH_API_ENDPOINT}/me/events"

        event = {
            'subject': summary,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC'
            }
        }

        if description:
            event['body'] = {
                'contentType': 'text',
                'content': description
            }
        if location:
            event['location'] = {
                'displayName': location
            }
        if attendees:
            event['attendees'] = [
                {
                    'emailAddress': {'address': email},
                    'type': 'required'
                }
                for email in attendees
            ]

        response = requests.post(url, headers=self._get_headers(), json=event)
        response.raise_for_status()

        return response.json()

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
        url = f"{self.GRAPH_API_ENDPOINT}/me/events/{event_id}"

        event_update = {}
        
        if summary:
            event_update['subject'] = summary
        if start_time:
            event_update['start'] = {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC'
            }
        if end_time:
            event_update['end'] = {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC'
            }
        if description:
            event_update['body'] = {
                'contentType': 'text',
                'content': description
            }
        if location:
            event_update['location'] = {
                'displayName': location
            }

        response = requests.patch(url, headers=self._get_headers(), json=event_update)
        response.raise_for_status()

        return response.json()

    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event.
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            bool: True if deletion successful, False otherwise.
        """
        try:
            url = f"{self.GRAPH_API_ENDPOINT}/me/events/{event_id}"
            response = requests.delete(url, headers=self._get_headers())
            response.raise_for_status()
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
        url = f"{self.GRAPH_API_ENDPOINT}/me/events"
        params = {
            '$search': f'"{query}"',
            '$top': max_results,
            '$orderby': 'start/dateTime'
        }

        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()

        return response.json().get('value', [])
