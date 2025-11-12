"""Tests for Google Calendar assistant."""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from calendar_assistant.google_calendar import GoogleCalendarAssistant
from calendar_assistant.base import CalendarAssistant


class TestGoogleCalendarAssistant(unittest.TestCase):
    """Test cases for GoogleCalendarAssistant class."""

    def test_inherits_from_base(self):
        """Test that GoogleCalendarAssistant inherits from CalendarAssistant."""
        self.assertTrue(issubclass(GoogleCalendarAssistant, CalendarAssistant))

    def test_initialization(self):
        """Test GoogleCalendarAssistant initialization."""
        assistant = GoogleCalendarAssistant(
            credentials_path='test_creds.json',
            token_path='test_token.pickle'
        )
        self.assertEqual(assistant.credentials_path, 'test_creds.json')
        self.assertEqual(assistant.token_path, 'test_token.pickle')
        self.assertIsNone(assistant.service)
        self.assertIsNone(assistant.creds)

    def test_has_required_scopes(self):
        """Test that GoogleCalendarAssistant has required scopes."""
        self.assertIsInstance(GoogleCalendarAssistant.SCOPES, list)
        self.assertIn('https://www.googleapis.com/auth/calendar', GoogleCalendarAssistant.SCOPES)

    @patch('calendar_assistant.google_calendar.build')
    @patch('calendar_assistant.google_calendar.os.path.exists')
    @patch('builtins.open', create=True)
    @patch('calendar_assistant.google_calendar.pickle.load')
    def test_authenticate_with_existing_token(self, mock_pickle_load, mock_open, mock_exists, mock_build):
        """Test authentication with existing valid token."""
        # Setup mocks
        mock_exists.return_value = True
        mock_creds = Mock()
        mock_creds.valid = True
        mock_pickle_load.return_value = mock_creds
        
        assistant = GoogleCalendarAssistant()
        result = assistant.authenticate()
        
        self.assertTrue(result)
        self.assertIsNotNone(assistant.service)
        mock_build.assert_called_once()

    def test_list_events_requires_authentication(self):
        """Test that list_events raises error when not authenticated."""
        assistant = GoogleCalendarAssistant()
        
        with self.assertRaises(RuntimeError) as context:
            assistant.list_events()
        
        self.assertIn("Not authenticated", str(context.exception))

    def test_create_event_requires_authentication(self):
        """Test that create_event raises error when not authenticated."""
        assistant = GoogleCalendarAssistant()
        start_time = datetime.utcnow()
        end_time = start_time + timedelta(hours=1)
        
        with self.assertRaises(RuntimeError) as context:
            assistant.create_event("Test Event", start_time, end_time)
        
        self.assertIn("Not authenticated", str(context.exception))


if __name__ == '__main__':
    unittest.main()
