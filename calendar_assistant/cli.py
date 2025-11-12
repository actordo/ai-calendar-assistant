"""Command-line interface for the calendar assistant."""

import argparse
import sys
from datetime import datetime, timedelta
from typing import Optional

from .google_calendar import GoogleCalendarAssistant
from .outlook_calendar import OutlookCalendarAssistant


def format_event(event: dict, calendar_type: str) -> str:
    """Format an event for display.
    
    Args:
        event: Event dictionary
        calendar_type: Type of calendar ('google' or 'outlook')
        
    Returns:
        Formatted event string
    """
    if calendar_type == 'google':
        summary = event.get('summary', 'No Title')
        start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', 'N/A'))
        location = event.get('location', 'No location')
        event_id = event.get('id', 'N/A')
    else:  # outlook
        summary = event.get('subject', 'No Title')
        start = event.get('start', {}).get('dateTime', 'N/A')
        location = event.get('location', {}).get('displayName', 'No location')
        event_id = event.get('id', 'N/A')
    
    return f"- {summary}\n  Time: {start}\n  Location: {location}\n  ID: {event_id}"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AI Calendar Assistant for Outlook and Google Calendar'
    )
    
    parser.add_argument(
        '--calendar',
        choices=['google', 'outlook'],
        required=True,
        help='Calendar type to use'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List events command
    list_parser = subparsers.add_parser('list', help='List calendar events')
    list_parser.add_argument('--days', type=int, default=7, help='Number of days to list (default: 7)')
    list_parser.add_argument('--max', type=int, default=10, help='Maximum number of events (default: 10)')
    
    # Create event command
    create_parser = subparsers.add_parser('create', help='Create a new event')
    create_parser.add_argument('--title', required=True, help='Event title')
    create_parser.add_argument('--start', required=True, help='Start time (ISO format: YYYY-MM-DDTHH:MM:SS)')
    create_parser.add_argument('--end', required=True, help='End time (ISO format: YYYY-MM-DDTHH:MM:SS)')
    create_parser.add_argument('--description', help='Event description')
    create_parser.add_argument('--location', help='Event location')
    create_parser.add_argument('--attendees', nargs='+', help='Attendee email addresses')
    
    # Update event command
    update_parser = subparsers.add_parser('update', help='Update an existing event')
    update_parser.add_argument('--event-id', required=True, help='Event ID to update')
    update_parser.add_argument('--title', help='New event title')
    update_parser.add_argument('--start', help='New start time (ISO format)')
    update_parser.add_argument('--end', help='New end time (ISO format)')
    update_parser.add_argument('--description', help='New event description')
    update_parser.add_argument('--location', help='New event location')
    
    # Delete event command
    delete_parser = subparsers.add_parser('delete', help='Delete an event')
    delete_parser.add_argument('--event-id', required=True, help='Event ID to delete')
    
    # Search events command
    search_parser = subparsers.add_parser('search', help='Search for events')
    search_parser.add_argument('--query', required=True, help='Search query')
    search_parser.add_argument('--max', type=int, default=10, help='Maximum number of results (default: 10)')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize calendar assistant
    try:
        if args.calendar == 'google':
            assistant = GoogleCalendarAssistant()
        else:  # outlook
            assistant = OutlookCalendarAssistant()
        
        print(f"Authenticating with {args.calendar.capitalize()} Calendar...")
        if not assistant.authenticate():
            print("Authentication failed!")
            return 1
        print("Authentication successful!\n")
        
    except Exception as e:
        print(f"Error initializing calendar assistant: {e}")
        return 1
    
    # Execute command
    try:
        if args.command == 'list':
            print(f"Listing events for the next {args.days} days...\n")
            start_time = datetime.utcnow()
            end_time = start_time + timedelta(days=args.days)
            events = assistant.list_events(start_time, end_time, args.max)
            
            if not events:
                print("No events found.")
            else:
                print(f"Found {len(events)} event(s):\n")
                for event in events:
                    print(format_event(event, args.calendar))
                    print()
        
        elif args.command == 'create':
            print("Creating new event...\n")
            start_time = datetime.fromisoformat(args.start)
            end_time = datetime.fromisoformat(args.end)
            
            event = assistant.create_event(
                summary=args.title,
                start_time=start_time,
                end_time=end_time,
                description=args.description,
                location=args.location,
                attendees=args.attendees
            )
            
            print("Event created successfully!")
            print(format_event(event, args.calendar))
        
        elif args.command == 'update':
            print("Updating event...\n")
            
            kwargs = {'event_id': args.event_id}
            if args.title:
                kwargs['summary'] = args.title
            if args.start:
                kwargs['start_time'] = datetime.fromisoformat(args.start)
            if args.end:
                kwargs['end_time'] = datetime.fromisoformat(args.end)
            if args.description:
                kwargs['description'] = args.description
            if args.location:
                kwargs['location'] = args.location
            
            event = assistant.update_event(**kwargs)
            print("Event updated successfully!")
            print(format_event(event, args.calendar))
        
        elif args.command == 'delete':
            print("Deleting event...\n")
            if assistant.delete_event(args.event_id):
                print("Event deleted successfully!")
            else:
                print("Failed to delete event.")
                return 1
        
        elif args.command == 'search':
            print(f"Searching for events matching '{args.query}'...\n")
            events = assistant.search_events(args.query, args.max)
            
            if not events:
                print("No events found.")
            else:
                print(f"Found {len(events)} event(s):\n")
                for event in events:
                    print(format_event(event, args.calendar))
                    print()
        
        return 0
        
    except Exception as e:
        print(f"Error executing command: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
