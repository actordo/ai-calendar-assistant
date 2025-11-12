from setuptools import setup, find_packages

setup(
    name="ai-calendar-assistant",
    version="0.1.0",
    description="AI Calendar Assistant for Outlook and Google Calendar",
    author="actordo",
    packages=find_packages(),
    install_requires=[
        "google-auth-oauthlib>=1.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-api-python-client>=2.0.0",
        "msal>=1.20.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "calendar-assistant=calendar_assistant.cli:main",
        ],
    },
)
