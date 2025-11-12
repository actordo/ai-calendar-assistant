"""Example usage of Outlook Calendar Assistant."""

import os
from datetime import datetime, timedelta
from calendar_assistant import OutlookCalendarAssistant


def main():
    """Demonstrate Outlook Calendar Assistant usage."""
    # Initialize the assistant
    # You can also set OUTLOOK_CLIENT_ID in environment variables
    client_id = os.getenv('OUTLOOK_CLIENT_ID', 'your_client_id_here')
    
    assistant = OutlookCalendarAssistant(
        client_id=client_id,
        token_cache_path='outlook_token.json'
    )
    
    # Authenticate
    print("Authenticating with Outlook Calendar...")
    if not assistant.authenticate():
        print("Authentication failed!")
        return
    print("Authentication successful!\n")
    
    # List upcoming events
    print("Listing upcoming events:")
    events = assistant.list_events(max_results=5)
    for event in events:
        start = event['start'].get('dateTime', 'N/A')
        print(f"- {event['subject']} at {start}")
    print()
    
    # Create a new event
    print("Creating a new event...")
    start_time = datetime.utcnow() + timedelta(days=1)
    end_time = start_time + timedelta(hours=1)
    
    new_event = assistant.create_event(
        summary="Team Standup",
        start_time=start_time,
        end_time=end_time,
        description="Daily standup meeting",
        location="Virtual - Teams",
        attendees=["team@example.com"]
    )
    print(f"Created event: {new_event['subject']} (ID: {new_event['id']})\n")
    
    # Search for events
    print("Searching for 'standup' events:")
    search_results = assistant.search_events("standup", max_results=3)
    for event in search_results:
        print(f"- {event['subject']}")
    print()
    
    # Update the event
    print("Updating the event...")
    updated_event = assistant.update_event(
        event_id=new_event['id'],
        summary="Team Standup - Updated",
        description="Daily standup meeting with sprint updates"
    )
    print(f"Updated event: {updated_event['subject']}\n")
    
    # Delete the event
    print("Deleting the event...")
    if assistant.delete_event(new_event['id']):
        print("Event deleted successfully!")
    else:
        print("Failed to delete event.")


if __name__ == '__main__':
    main()
