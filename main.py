"""
Enigma2 Extension - Movie & Series Library
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.enigma2_handler import Enigma2Handler
from src.core.content_fetcher import ContentFetcher
from src.utils.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)


class Enigma2Extension:
    """Main class for Enigma2 Extension"""
    
    def __init__(self):
        """Initialize the extension"""
        self.enigma2 = Enigma2Handler()
        self.fetcher = ContentFetcher()
        logger.info("Enigma2 Extension initialized")
    
    def start(self):
        """Start the extension"""
        try:
            logger.info("Starting Enigma2 Extension - Movie & Series Library")
            print("=" * 50)
            print("Enigma2 Extension - Movie & Series Library")
            print("=" * 50)
            self.show_menu()
        except Exception as e:
            logger.error(f"Error starting extension: {e}")
            print(f"Error: {e}")
    
    def show_menu(self):
        """Display main menu"""
        while True:
            print("\nMain Menu:")
            print("1. Search for Movies")
            print("2. Search for Series")
            print("3. Search for Programs")
            print("4. View Favorites")
            print("5. Settings")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                self.search_movies()
            elif choice == "2":
                self.search_series()
            elif choice == "3":
                self.search_programs()
            elif choice == "4":
                self.view_favorites()
            elif choice == "5":
                self.settings()
            elif choice == "6":
                logger.info("Exiting Enigma2 Extension")
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")
    
    def search_movies(self):
        """Search for movies"""
        print("\n--- Search Movies ---")
        query = input("Enter movie name: ").strip()
        if query:
            logger.info(f"Searching for movies: {query}")
            print(f"Searching for: {query}...")
            # TODO: Implement movie search
            print("Feature coming soon!")
    
    def search_series(self):
        """Search for series"""
        print("\n--- Search Series ---")
        query = input("Enter series name: ").strip()
        if query:
            logger.info(f"Searching for series: {query}")
            print(f"Searching for: {query}...")
            # TODO: Implement series search
            print("Feature coming soon!")
    
    def search_programs(self):
        """Search for programs"""
        print("\n--- Search Programs ---")
        query = input("Enter program name: ").strip()
        if query:
            logger.info(f"Searching for programs: {query}")
            print(f"Searching for: {query}...")
            # TODO: Implement program search
            print("Feature coming soon!")
    
    def view_favorites(self):
        """View favorite content"""
        print("\n--- Favorites ---")
        # TODO: Implement favorites
        print("Feature coming soon!")
    
    def settings(self):
        """Show settings menu"""
        print("\n--- Settings ---")
        # TODO: Implement settings
        print("Feature coming soon!")


def main():
    """Main entry point"""
    try:
        extension = Enigma2Extension()
        extension.start()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        print("\n\nApplication interrupted by user")
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        print(f"Critical error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()