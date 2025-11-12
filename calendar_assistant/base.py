"""Base calendar assistant interface."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional


class CalendarAssistant(ABC):
    """Abstract base class for calendar assistants."""

    @abstractmethod
    def authenticate(self) -> bool:
        """Authenticate with the calendar service.
        
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def delete_event(self, event_id: str) -> bool:
        """Delete a calendar event.
        
        Args:
            event_id: ID of the event to delete
            
        Returns:
            bool: True if deletion successful, False otherwise.
        """
        pass

    @abstractmethod
    def search_events(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search for calendar events by query string.
        
        Args:
            query: Search query string
            max_results: Maximum number of events to return
            
        Returns:
            List of matching event dictionaries
        """
        pass
