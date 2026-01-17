#!/usr/bin/env python3
"""
Canopus - Main Entry Point
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    """Main entry point for the application"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Canopus")
    app.setOrganizationName("Constellation Apps")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
