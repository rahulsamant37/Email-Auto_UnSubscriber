"""Gmail connection and email processing functions."""
import imaplib
import email
import os
from bs4 import BeautifulSoup
import tldextract

from src.processor.link_processor import extract_links_from_html, extract_company_name

def connect_to_mail():
    """
    Establish a connection to Gmail using IMAP.
    
    Returns:
        imaplib.IMAP4_SSL: An authenticated IMAP connection object or None if connection fails
    """
    username = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    try:
        print(f"Connecting to Gmail as {username}...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(username, password)
        mail.select("inbox")
        print("Successfully connected to Gmail")
        return mail
    except imaplib.IMAP4.error as e:
        error_msg = str(e)
        if "Application-specific password required" in error_msg:
            print("\nERROR: Gmail requires an app password for this script.")
            print("1. Enable 2-Step Verification: https://myaccount.google.com/security")
            print("2. Generate an app password: https://myaccount.google.com/apppasswords")
            print("3. Update your .env file with the new app password")
        else:
            print(f"\nERROR: Failed to connect to Gmail: {error_msg}")
        return None
    except Exception as e:
        print(f"\nERROR: Unexpected error connecting to Gmail: {str(e)}")
        return None

def group_links_by_service(links):
    """
    Group unsubscribe links by service domain and select best candidate
    
    Args:
        links (list): List of unsubscribe URLs
        
    Returns:
        dict: Dictionary with domain as key and service info as value
    """
    service_map = {}
    
    for link in links:
        try:
            # Extract root domain using tldextract
            parsed = tldextract.extract(link)
            domain_key = f"{parsed.domain}.{parsed.suffix}"
            
            # Get company name
            company_name = extract_company_name(link)
            
            # Track best candidate per service
            if domain_key not in service_map or \
               len(link) < len(service_map[domain_key]['url']):
                service_map[domain_key] = {
                    'url': link,
                    'company': company_name,
                    'domain': domain_key,
                    'count': 1
                }
            else:
                service_map[domain_key]['count'] += 1
                
        except Exception as e:
            print(f"Error processing {link}: {str(e)}")
    
    print(f"Found {len(service_map)} unique services")
    return service_map

def search_for_email():
    """
    Search Gmail inbox for emails containing unsubscribe links.
    
    Returns:
        dict: Dictionary of unique services with their unsubscribe URLs
    """
    # Connect to Gmail and search for emails containing "unsubscribe"
    mail = connect_to_mail()
    if not mail:
        return {}
    
    try:
        print("Searching for emails with 'unsubscribe' text...")
        _, search_data = mail.search(None, '(BODY "unsubscribe")')
        data = search_data[0].split()
        
        if not data:
            print("No emails found with 'unsubscribe' text")
            mail.logout()
            return {}
            
        print(f"Found {len(data)} emails to process")
        links = []
        
        # Process each email found
        for i, num in enumerate(data):
            try:
                print(f"Processing email {i+1}/{len(data)}...", end="\r")
                _, data = mail.fetch(num, "(RFC822)")
                msg = email.message_from_bytes(data[0][1])
                
                # Handle multipart messages (emails with both HTML and text content)
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/html":
                            try:
                                payload = part.get_payload(decode=True)
                                charset = part.get_content_charset() or 'utf-8'
                                html_content = payload.decode(charset, errors='ignore')
                                links.extend(extract_links_from_html(html_content))
                            except Exception as e:
                                print(f"\nError processing multipart message: {str(e)}")
                                continue
                else:
                    # Handle single part messages
                    content_type = msg.get_content_type()
                    if content_type == "text/html":
                        try:
                            payload = msg.get_payload(decode=True)
                            charset = msg.get_content_charset() or 'utf-8'
                            content = payload.decode(charset, errors='ignore')
                            links.extend(extract_links_from_html(content))
                        except Exception as e:
                            print(f"\nError processing single part message: {str(e)}")
                            continue
            except Exception as e:
                print(f"\nError processing email: {str(e)}")
                continue
        
        print("\nEmail processing complete")
        mail.logout()
        
        # Remove duplicates and group by service
        return group_links_by_service(list(set(links)))
        
    except Exception as e:
        print(f"Error searching for emails: {str(e)}")
        try:
            mail.logout()
        except:
            pass
        return {}