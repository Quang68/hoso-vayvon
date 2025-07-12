#!/usr/bin/env python3
"""
Script to check OAuth2 email address
"""
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def check_oauth_email():
    """Check the email address of the OAuth2 authenticated user"""
    try:
        # Load credentials from token.json
        with open('token.json', 'r') as f:
            token_data = json.load(f)
        
        # Create credentials object
        credentials = Credentials(
            token=token_data['token'],
            refresh_token=token_data['refresh_token'],
            token_uri=token_data['token_uri'],
            client_id=token_data['client_id'],
            client_secret=token_data['client_secret'],
            scopes=token_data['scopes']
        )
        
        # Build the People API service
        service = build('people', 'v1', credentials=credentials)
        
        # Get profile information
        profile = service.people().get(
            resourceName='people/me',
            personFields='emailAddresses,names'
        ).execute()
        
        print("OAuth2 Account Information:")
        print("=" * 50)
        
        # Get email addresses
        if 'emailAddresses' in profile:
            for email in profile['emailAddresses']:
                print(f"Email: {email['value']}")
                if email.get('metadata', {}).get('primary', False):
                    print(f"Primary Email: {email['value']}")
        
        # Get names
        if 'names' in profile:
            for name in profile['names']:
                if name.get('metadata', {}).get('primary', False):
                    print(f"Name: {name['displayName']}")
        
        print("\nNote: You need to add this email to Test Users in Google Cloud Console")
        print("Then share the template file with this email address")
        
    except Exception as e:
        print(f"Error checking OAuth2 email: {str(e)}")
        print("\nAlternative method:")
        print("1. Go to https://myaccount.google.com/")
        print("2. Check the email address displayed at the top")
        print("3. This is the email you used for OAuth2 authentication")

if __name__ == "__main__":
    check_oauth_email()
