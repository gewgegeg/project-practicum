import requests
from django.conf import settings


class LinkedInClient:
    def __init__(self):
        self.client_id = settings.LINKEDIN_CLIENT_ID
        self.client_secret = settings.LINKEDIN_CLIENT_SECRET
        self.redirect_uri = settings.LINKEDIN_REDIRECT_URI

    def get_authorization_url(self):
        return f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=r_liteprofile%20r_emailaddress"

    def get_access_token(self, code):
        response = requests.post(
            'https://www.linkedin.com/oauth/v2/accessToken',
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
            }
        )
        return response.json()

    def get_profile(self, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(
            'https://api.linkedin.com/v2/me',
            headers=headers
        )
        return response.json()
