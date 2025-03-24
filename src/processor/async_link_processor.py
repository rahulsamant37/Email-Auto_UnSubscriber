"""Asynchronous link processing utilities."""
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import tldextract
from src.processor.link_processor import extract_company_name, extract_links_from_html

async def click_link_async(session, link):
    """
    Asynchronously visit an unsubscribe link and report the result.
    
    Args:
        session (aiohttp.ClientSession): Async HTTP session
        link (str): URL to visit for unsubscription
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"Visiting: {link}")
        async with session.get(link, timeout=10) as response:
            if response.status == 200:
                print("✓ Successfully visited")
                return True
            else:
                print(f"✗ Failed with status code {response.status}")
                return False
    except asyncio.TimeoutError:
        print("✗ Request timed out")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

async def process_links_concurrently(service_map, max_concurrent=5):
    """
    Process multiple unsubscribe links concurrently.
    
    Args:
        service_map (dict): Dictionary of services with their unsubscribe URLs
        max_concurrent (int): Maximum number of concurrent requests
        
    Returns:
        int: Number of successful unsubscriptions
    """
    success_count = 0
    
    # Create a semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_link(session, domain, service_info):
        async with semaphore:
            if await click_link_async(session, service_info['url']):
                return 1
            return 0
    
    # Create client session for all requests
    async with aiohttp.ClientSession() as session:
        # Create tasks for all links
        tasks = []
        for domain, service_info in service_map.items():
            task = asyncio.create_task(
                process_link(session, domain, service_info)
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks)
        success_count = sum(results)
    
    return success_count