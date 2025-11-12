"""Example usage of Google Calendar Assistant."""

from datetime import datetime, timedelta
from calendar_assistant import GoogleCalendarAssistant


def main():
    """Demonstrate Google Calendar Assistant usage."""
    # Initialize the assistant
    assistant = GoogleCalendarAssistant(
        credentials_path='credentials.json',
        token_path='token.pickle'
    )
    
    # Authenticate
    print("Authenticating with Google Calendar...")
    if not assistant.authenticate():
        print("Authentication failed!")
        return
    print("Authentication successful!\n")
    
    # List upcoming events
    print("Listing upcoming events:")
    events = assistant.list_events(max_results=5)
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"- {event['summary']} at {start}")
    print()
    
    # Create a new event
    print("Creating a new event...")
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    new_event = assistant.create_event(
        summary="Team Meeting",
        start_time=start_time,
        end_time=end_time,
        description="Discuss project updates",
        location="Conference Room A",
        attendees=["team@example.com"]
    )
    print(f"Created event: {new_event['summary']} (ID: {new_event['id']})\n")
    
    # Search for events
    print("Searching for 'meeting' events:")
    search_results = assistant.search_events("meeting", max_results=3)
    for event in search_results:
        print(f"- {event['summary']}")
    print()
    
    # Update the event
    print("Updating the event...")
    updated_event = assistant.update_event(
        event_id=new_event['id'],
        summary="Team Meeting - Updated",
        description="Discuss project updates and Q4 planning"
    )
    print(f"Updated event: {updated_event['summary']}\n")
    
    # Delete the event
    print("Deleting the event...")
    if assistant.delete_event(new_event['id']):
        print("Event deleted successfully!")
    else:
        print("Failed to delete event.")


if __name__ == '__main__':
    main()
