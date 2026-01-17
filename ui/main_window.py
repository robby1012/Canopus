"""
Main window for Canopus application
"""
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QMessageBox, QApplication
from PyQt6.QtCore import Qt
from services.cosmos_db_service import CosmosDBService
from ui.sidebar import Sidebar
from ui.table_view import FilterableTableView


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.db_service = CosmosDBService()
        self.current_database = None
        self.current_container = None
        
        self.setup_ui()
        self.setup_window()
    
    def setup_window(self):
        """Setup window properties"""
        self.setWindowTitle("Canopus - Azure Cosmos DB Browser")
        
        # Set window to open maximized (fullscreen)
        self.showMaximized()
        
        # Minimum size
        self.setMinimumSize(800, 600)
    
    def setup_ui(self):
        """Setup the UI components"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout - horizontal split
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Sidebar (25% width)
        self.sidebar = Sidebar(self.db_service)
        self.sidebar.container_selected.connect(self.handle_container_selected)
        main_layout.addWidget(self.sidebar, 1)  # Weight 1 for 25%
        
        # Table view (75% width)
        self.table_view = FilterableTableView()
        main_layout.addWidget(self.table_view, 3)  # Weight 3 for 75%
    
    def handle_container_selected(self, database: str, container: str):
        """
        Handle when a container is selected in the sidebar
        
        Args:
            database: Name of the database
            container: Name of the container
        """
        self.current_database = database
        self.current_container = container
        
        # Update window title
        self.setWindowTitle(f"Azure Cosmos DB Browser - {database}/{container}")
        
        # Load data from container
        self.load_container_data(database, container)
    
    def load_container_data(self, database: str, container: str):
        """
        Load data from a container into the table view
        
        Args:
            database: Name of the database
            container: Name of the container
        """
        try:
            # Show loading message
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
            
            # Fetch data
            items = self.db_service.get_all_items(database, container, max_items=1000)
            
            # Load into table
            self.table_view.load_data(items)
            
            # Restore cursor
            QApplication.restoreOverrideCursor()
            
            if not items:
                QMessageBox.information(
                    self,
                    "No Data",
                    f"Container '{container}' is empty or no items could be retrieved."
                )
        
        except Exception as e:
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(
                self,
                "Error Loading Data",
                f"Failed to load data from container:\n{str(e)}"
            )
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Disconnect from database
        if self.db_service.connected:
            self.db_service.disconnect()
        
        event.accept()
