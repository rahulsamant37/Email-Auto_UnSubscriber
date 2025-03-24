"""File operation utilities for saving links."""
import csv

def save_links(service_map):
    """
    Save the found unsubscribe links to text and CSV files.
    
    Args:
        service_map (dict): Dictionary of services with their unsubscribe URLs
    """
    if not service_map:
        print("No links to save")
        return
    
    # Extract list of links for text file
    links = [service_info['url'] for service_info in service_map.values()]
        
    # Save to text file
    try:
        with open("unsubscribe_links.txt", "w") as f:
            f.write("\n".join(links))
        print(f"Saved {len(links)} links to unsubscribe_links.txt")
    except Exception as e:
        print(f"Error saving links to text file: {str(e)}")
    
    # Save to CSV file with company names
    try:
        # Use semicolon delimiter and add BOM for Excel compatibility
        with open("unsubscribe_services.csv", "w", newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['company', 'domain', 'url', 'emails_found']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            writer.writeheader()
            for service_info in service_map.values():
                writer.writerow({
                    'company': service_info['company'],
                    'domain': service_info['domain'],
                    'url': service_info['url'],
                    'emails_found': service_info['count']
                })
        print(f"Saved {len(service_map)} services to unsubscribe_services.csv")
    except Exception as e:
        print(f"Error saving to CSV file: {str(e)}")