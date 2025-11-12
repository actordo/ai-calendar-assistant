"""Tests for the base calendar assistant class."""

import unittest
from abc import ABC
from calendar_assistant.base import CalendarAssistant


class TestCalendarAssistantBase(unittest.TestCase):
    """Test cases for the base CalendarAssistant class."""

    def test_is_abstract(self):
        """Test that CalendarAssistant is an abstract base class."""
        self.assertTrue(issubclass(CalendarAssistant, ABC))

    def test_cannot_instantiate(self):
        """Test that CalendarAssistant cannot be directly instantiated."""
        with self.assertRaises(TypeError):
            CalendarAssistant()

    def test_has_required_methods(self):
        """Test that CalendarAssistant defines all required abstract methods."""
        required_methods = [
            'authenticate',
            'list_events',
            'create_event',
            'update_event',
            'delete_event',
            'search_events'
        ]
        
        for method_name in required_methods:
            self.assertTrue(
                hasattr(CalendarAssistant, method_name),
                f"CalendarAssistant should have {method_name} method"
            )


if __name__ == '__main__':
    unittest.main()
