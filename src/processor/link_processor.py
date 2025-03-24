"""Link extraction and processing utilities."""
import requests
from bs4 import BeautifulSoup
import tldextract

def extract_links_from_html(html_content):
    """
    Parse HTML content and extract unsubscribe links.
    
    Args:
        html_content (str): HTML content of the email
        
    Returns:
        list: List of unsubscribe URLs found in the HTML content
    """
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        links = [link["href"] for link in soup.find_all("a", href=True) if "unsubscribe" in link["href"].lower()]
        return links
    except Exception as e:
        print(f"Error parsing HTML content: {str(e)}")
        return []

def click_link(link):
    """
    Visit an unsubscribe link and report the result.
    
    Args:
        link (str): URL to visit for unsubscription
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Visiting: {link}")
        response = requests.get(link, timeout=10)
        if response.status_code == 200:
            print("✓ Successfully visited")
            return True
        else:
            print(f"✗ Failed with status code {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print("✗ Request timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("✗ Connection error")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def extract_company_name(url):
    """
    Extract company name from URL domain
    
    Args:
        url (str): URL to extract company name from
        
    Returns:
        str: Company name
    """
    try:
        # Extract domain information
        extracted = tldextract.extract(url)
        
        # Use domain as company name, capitalize first letter
        company = extracted.domain.replace('-', ' ').replace('_', ' ')
        company = company.title()
        
        return company
    except Exception:
        return "Unknown"