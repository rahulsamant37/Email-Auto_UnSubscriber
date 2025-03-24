#!/usr/bin/env python3
"""
Auto Email Unsubscriber

This script automatically finds and clicks unsubscribe links from emails in your Gmail inbox.
"""
from dotenv import load_dotenv
import sys

from src.config.config import check_env_variables
from src.connector.gmail_connector import search_for_email
from src.processor.async_link_processor import process_links_concurrently
from src.utils.file_utils import save_links

async def main():
    print("=" * 50)
    print("Auto Email Unsubscriber")
    print("=" * 50)
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check if environment variables are set
    if not check_env_variables():
        print("\nPlease set the required environment variables in the .env file:")
        print("EMAIL=your.email@gmail.com")
        print("PASSWORD=your-app-password")
        print("\nNote: Gmail requires an app password, not your regular password.")
        print("Get an app password at: https://myaccount.google.com/apppasswords")
        sys.exit(1)
    
    # Find all unsubscribe links
    service_map = search_for_email()
    
    if service_map:
        print("\nVisiting unsubscribe links concurrently...")
        # Visit unsubscribe links concurrently
        success_count = await process_links_concurrently(service_map)
        
        # Save links for reference
        print("\nSaving links for reference...")
        save_links(service_map)
        
        print(f"\nUnsubscribe process complete! Successfully visited {success_count}/{len(service_map)} links.")
    else:
        print("\nNo unsubscribe links found. Process complete.")

