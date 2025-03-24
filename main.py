#!/usr/bin/env python3
"""
Auto Email Unsubscriber

This script automatically finds and clicks unsubscribe links from emails in your Gmail inbox.
"""
from src.app import main
import asyncio


# Main execution
if __name__ == "__main__":
    asyncio.run(main())