# AI Calendar Assistant

A powerful Python-based calendar assistant that seamlessly integrates with both **Google Calendar** and **Outlook Calendar** (via Microsoft Graph API). This tool provides a unified interface to manage your calendar events across both platforms.

## Features

- 🗓️ **Multi-Platform Support**: Works with both Google Calendar and Outlook Calendar
- 📝 **Event Management**: Create, read, update, and delete calendar events
- 🔍 **Search Functionality**: Search for events by keywords
- 🖥️ **CLI Interface**: Easy-to-use command-line interface
- 🐍 **Python API**: Programmable interface for custom integrations
- 🔐 **Secure Authentication**: OAuth 2.0 authentication for both platforms

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from source

```bash
git clone https://github.com/actordo/ai-calendar-assistant.git
cd ai-calendar-assistant
pip install -r requirements.txt
pip install -e .
```

## Setup

### Google Calendar Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download the credentials and save as `credentials.json` in your project directory

### Outlook Calendar Setup

1. Go to the [Azure Portal](https://portal.azure.com/)
2. Register a new application in Azure AD
3. Add the following API permissions:
   - Microsoft Graph → Calendars.ReadWrite (Delegated)
4. Copy your Application (client) ID
5. Create a `.env` file and add:
   ```
   OUTLOOK_CLIENT_ID=your_client_id_here
   ```

## Usage

### Command-Line Interface

#### List Events

**Google Calendar:**
```bash
calendar-assistant --calendar google list --days 7 --max 10
```

**Outlook Calendar:**
```bash
calendar-assistant --calendar outlook list --days 7 --max 10
```

#### Create an Event

**Google Calendar:**
```bash
calendar-assistant --calendar google create \
  --title "Team Meeting" \
  --start "2025-11-15T14:00:00" \
  --end "2025-11-15T15:00:00" \
  --description "Discuss project updates" \
  --location "Conference Room A" \
  --attendees person1@example.com person2@example.com
```

**Outlook Calendar:**
```bash
calendar-assistant --calendar outlook create \
  --title "Team Meeting" \
  --start "2025-11-15T14:00:00" \
  --end "2025-11-15T15:00:00" \
  --description "Discuss project updates" \
  --location "Conference Room A"
```

#### Update an Event

```bash
calendar-assistant --calendar google update \
  --event-id "event_id_here" \
  --title "Updated Meeting Title" \
  --location "Conference Room B"
```

#### Delete an Event

```bash
calendar-assistant --calendar google delete --event-id "event_id_here"
```

#### Search Events

```bash
calendar-assistant --calendar google search --query "meeting" --max 5
```

### Python API

#### Google Calendar Example

```python
from datetime import datetime, timedelta
from calendar_assistant import GoogleCalendarAssistant

# Initialize and authenticate
assistant = GoogleCalendarAssistant()
assistant.authenticate()

# List upcoming events
events = assistant.list_events(max_results=5)
for event in events:
    print(event['summary'])

# Create an event
start_time = datetime.utcnow() + timedelta(days=1)
end_time = start_time + timedelta(hours=1)

new_event = assistant.create_event(
    summary="Team Meeting",
    start_time=start_time,
    end_time=end_time,
    description="Discuss project updates",
    location="Conference Room A"
)

# Search events
results = assistant.search_events("meeting", max_results=5)

# Update an event
assistant.update_event(
    event_id=new_event['id'],
    summary="Updated Meeting Title"
)

# Delete an event
assistant.delete_event(new_event['id'])
```

#### Outlook Calendar Example

```python
import os
from datetime import datetime, timedelta
from calendar_assistant import OutlookCalendarAssistant

# Initialize and authenticate
client_id = os.getenv('OUTLOOK_CLIENT_ID')
assistant = OutlookCalendarAssistant(client_id=client_id)
assistant.authenticate()

# List upcoming events
events = assistant.list_events(max_results=5)
for event in events:
    print(event['subject'])

# Create an event
start_time = datetime.utcnow() + timedelta(days=1)
end_time = start_time + timedelta(hours=1)

new_event = assistant.create_event(
    summary="Team Standup",
    start_time=start_time,
    end_time=end_time,
    description="Daily standup",
    location="Virtual - Teams"
)

# Search events
results = assistant.search_events("standup", max_results=5)

# Update an event
assistant.update_event(
    event_id=new_event['id'],
    summary="Updated Standup"
)

# Delete an event
assistant.delete_event(new_event['id'])
```

## API Reference

### Base CalendarAssistant Class

All calendar assistants implement the following methods:

- `authenticate()`: Authenticate with the calendar service
- `list_events(start_time, end_time, max_results)`: List events in a time range
- `create_event(summary, start_time, end_time, description, location, attendees)`: Create a new event
- `update_event(event_id, summary, start_time, end_time, description, location)`: Update an existing event
- `delete_event(event_id)`: Delete an event
- `search_events(query, max_results)`: Search for events by keyword

### GoogleCalendarAssistant

Specific implementation for Google Calendar using the Google Calendar API v3.

**Parameters:**
- `credentials_path`: Path to OAuth credentials file (default: 'credentials.json')
- `token_path`: Path to store authentication token (default: 'token.pickle')

### OutlookCalendarAssistant

Specific implementation for Outlook Calendar using Microsoft Graph API.

**Parameters:**
- `client_id`: Azure AD application client ID
- `client_secret`: Azure AD application client secret (optional)
- `token_cache_path`: Path to store token cache (default: 'outlook_token.json')

## Examples

Check the `examples/` directory for complete working examples:
- `google_example.py`: Google Calendar integration example
- `outlook_example.py`: Outlook Calendar integration example

## Security

- Never commit your credentials files (`credentials.json`, `token.pickle`, `outlook_token.json`, `.env`)
- All authentication tokens are stored locally and encrypted
- OAuth 2.0 ensures secure access to calendar data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/actordo/ai-calendar-assistant).