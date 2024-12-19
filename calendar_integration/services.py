# calendar_integration/services.py
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class GoogleCalendarService:
    @staticmethod
    def add_interview(user, interview_data):
        credentials = get_user_credentials(user)
        service = build('calendar', 'v3', credentials=credentials)
        
        event = {
            'summary': f"Interview for {interview_data['position']}",
            'location': interview_data['location'],
            'description': interview_data['description'],
            'start': {'dateTime': interview_data['start_time']},
            'end': {'dateTime': interview_data['end_time']},
        }
        
        return service.events().insert(calendarId='primary', body=event).execute()