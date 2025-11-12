"""Tests for Outlook Calendar assistant."""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from calendar_assistant.outlook_calendar import OutlookCalendarAssistant
from calendar_assistant.base import CalendarAssistant


class TestOutlookCalendarAssistant(unittest.TestCase):
    """Test cases for OutlookCalendarAssistant class."""

    def test_inherits_from_base(self):
        """Test that OutlookCalendarAssistant inherits from CalendarAssistant."""
        self.assertTrue(issubclass(OutlookCalendarAssistant, CalendarAssistant))

    def test_initialization_with_client_id(self):
        """Test OutlookCalendarAssistant initialization with client_id."""
        assistant = OutlookCalendarAssistant(
            client_id='test_client_id',
            token_cache_path='test_token.json'
        )
        self.assertEqual(assistant.client_id, 'test_client_id')
        self.assertEqual(assistant.token_cache_path, 'test_token.json')
        self.assertIsNone(assistant.access_token)

    def test_initialization_without_client_id_raises_error(self):
        """Test that initialization without client_id raises ValueError."""
        with self.assertRaises(ValueError) as context:
            OutlookCalendarAssistant()
        
        self.assertIn("client_id is required", str(context.exception))

    def test_has_required_scopes(self):
        """Test that OutlookCalendarAssistant has required scopes."""
        self.assertIsInstance(OutlookCalendarAssistant.SCOPES, list)
        self.assertIn('Calendars.ReadWrite', OutlookCalendarAssistant.SCOPES)

    def test_has_graph_api_endpoint(self):
        """Test that OutlookCalendarAssistant has Graph API endpoint."""
        self.assertEqual(
            OutlookCalendarAssistant.GRAPH_API_ENDPOINT,
            'https://graph.microsoft.com/v1.0'
        )

    def test_list_events_requires_authentication(self):
        """Test that list_events raises error when not authenticated."""
        assistant = OutlookCalendarAssistant(client_id='test_id')
        
        with self.assertRaises(RuntimeError) as context:
            assistant.list_events()
        
        self.assertIn("Not authenticated", str(context.exception))

    def test_create_event_requires_authentication(self):
        """Test that create_event raises error when not authenticated."""
        assistant = OutlookCalendarAssistant(client_id='test_id')
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(hours=1)
        
        with self.assertRaises(RuntimeError) as context:
            assistant.create_event("Test Event", start_time, end_time)
        
        self.assertIn("Not authenticated", str(context.exception))

    @patch('calendar_assistant.outlook_calendar.requests.get')
    def test_list_events_with_authentication(self, mock_get):
        """Test list_events with authentication."""
        assistant = OutlookCalendarAssistant(client_id='test_id')
        assistant.access_token = 'test_token'
        
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            'value': [
                {'subject': 'Test Event', 'id': '123'}
            ]
        }
        mock_get.return_value = mock_response
        
        events = assistant.list_events()
        
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]['subject'], 'Test Event')
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
