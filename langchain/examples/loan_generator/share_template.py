#!/usr/bin/env python3
"""
Script to share template file with OAuth2 email
"""
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def share_template_file():
    """Share the template file with OAuth2 email"""
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
        
        # Refresh token if needed
        if credentials.expired:
            credentials.refresh(Request())
            
        # Build the Drive API service
        service = build('drive', 'v3', credentials=credentials)
        
        # Template file ID
        template_file_id = '1DfGBOuJphBKgSR6nFjSP3-LMgY5uFnWJ'
        oauth_email = 'hovanquang176@gmail.com'
        
        # Check if file exists and get current permissions
        try:
            file_info = service.files().get(fileId=template_file_id, fields='name,permissions').execute()
            print(f"File found: {file_info.get('name', 'Unknown')}")
            print(f"Current permissions: {len(file_info.get('permissions', []))} permission(s)")
            
            # Check if the email already has access
            permissions = service.permissions().list(fileId=template_file_id).execute()
            has_access = False
            for perm in permissions.get('permissions', []):
                if perm.get('emailAddress') == oauth_email:
                    has_access = True
                    print(f"Email {oauth_email} already has access with role: {perm.get('role', 'unknown')}")
                    break
            
            if not has_access:
                # Share the file with the OAuth2 email
                permission = {
                    'type': 'user',
                    'role': 'reader',  # Can be 'reader', 'writer', or 'owner'
                    'emailAddress': oauth_email
                }
                
                result = service.permissions().create(
                    fileId=template_file_id,
                    body=permission,
                    fields='id'
                ).execute()
                
                print(f"Successfully shared file with {oauth_email}")
                print(f"Permission ID: {result.get('id')}")
            else:
                print(f"File is already shared with {oauth_email}")
                
        except Exception as e:
            if "404" in str(e):
                print(f"Error: File with ID {template_file_id} not found or not accessible")
                print("This might mean:")
                print("1. The file ID is incorrect")
                print("2. The file was created by a different account (Service Account)")
                print("3. The file has been deleted")
                print("\nSolution:")
                print("1. Upload a new template file using OAuth2 account")
                print("2. Update the TEMPLATE_FILE_ID in your code")
            else:
                print(f"Error accessing file: {str(e)}")
                
    except Exception as e:
        print(f"Error sharing file: {str(e)}")

if __name__ == "__main__":
    share_template_file()
