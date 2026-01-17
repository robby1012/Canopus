"""
Sidebar component with connection manager and navigation
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLineEdit, QPushButton,
    QListWidget, QLabel, QMessageBox, QListWidgetItem
)
from PyQt6.QtCore import pyqtSignal, Qt
from models.connection_config import ConnectionConfig
from services.cosmos_db_service import CosmosDBService
from services.connection_storage_service import ConnectionStorageService
from ui.connection_dialog import ConnectionDialog


class Sidebar(QWidget):
    """Sidebar with connection manager, database list, and container list"""
    
    # Signals
    database_selected = pyqtSignal(str)  # Emitted when a database is selected
    container_selected = pyqtSignal(str, str)  # Emitted with (database, container)
    
    def __init__(self, db_service: CosmosDBService, parent=None):
        super().__init__(parent)
        self.db_service = db_service
        self.storage_service = ConnectionStorageService()
        self.current_database = None
        
        self.setup_ui()
        self.load_saved_connections()
    
    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        
        # Saved Connections List with buttons
        self.saved_connections_group = self.create_saved_connections_list()
        layout.addWidget(self.saved_connections_group, 2)  # 20% weight
        
        # Database List
        self.database_group = self.create_database_list()
        layout.addWidget(self.database_group, 4)  # 40% weight
        
        # Container List
        self.container_group = self.create_container_list()
        layout.addWidget(self.container_group, 4)  # 40% weight
    
    def create_saved_connections_list(self) -> QGroupBox:
        """Create saved connections list section"""
        group = QGroupBox("Saved Connections")
        layout = QVBoxLayout()
        
        # Connections list
        self.saved_connections_list = QListWidget()
        layout.addWidget(self.saved_connections_list)
        
        # Buttons row
        button_layout = QHBoxLayout()
        
        # Connect button (left/center)
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.handle_connect)
        self.connect_btn.setToolTip("Connect to selected connection")
        button_layout.addWidget(self.connect_btn, 1)
        
        button_layout.addStretch()
        
        # Add button
        self.add_connection_btn = QPushButton("+")
        self.add_connection_btn.setFixedSize(30, 30)
        self.add_connection_btn.clicked.connect(self.handle_add_connection)
        self.add_connection_btn.setToolTip("Add new connection")
        button_layout.addWidget(self.add_connection_btn)
        
        # Remove button
        self.remove_connection_btn = QPushButton("-")
        self.remove_connection_btn.setFixedSize(30, 30)
        self.remove_connection_btn.clicked.connect(self.handle_remove_connection)
        self.remove_connection_btn.setToolTip("Remove selected connection")
        button_layout.addWidget(self.remove_connection_btn)
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Not connected")
        self.status_label.setStyleSheet("color: gray;")
        layout.addWidget(self.status_label)
        
        group.setLayout(layout)
        return group
    
    def create_database_list(self) -> QGroupBox:
        """Create database list section"""
        group = QGroupBox("Databases")
        layout = QVBoxLayout()
        
        self.database_list = QListWidget()
        self.database_list.itemClicked.connect(self.handle_database_selected)
        layout.addWidget(self.database_list)
        
        group.setLayout(layout)
        return group
    
    def create_container_list(self) -> QGroupBox:
        """Create container list section"""
        group = QGroupBox("Containers")
        layout = QVBoxLayout()
        
        self.container_list = QListWidget()
        self.container_list.itemClicked.connect(self.handle_container_selected)
        layout.addWidget(self.container_list)
        
        group.setLayout(layout)
        return group
    
    def handle_connect(self):
        """Handle connect button click"""
        current_item = self.saved_connections_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a connection to connect")
            return
        
        connection_id = current_item.data(Qt.ItemDataRole.UserRole)
        result = self.storage_service.get_connection(connection_id)
        
        if not result:
            QMessageBox.warning(self, "Error", "Failed to load connection")
            return
        
        name, config = result
        
        # Connect using the configuration
        success, message = self.db_service.connect(config)
        
        if success:
            self.status_label.setText(f"Connected: {name}")
            self.status_label.setStyleSheet("color: green;")
            self.connect_btn.setText("Disconnect")
            self.connect_btn.clicked.disconnect()
            self.connect_btn.clicked.connect(self.handle_disconnect)
            
            # Load databases
            self.load_databases()
        else:
            self.status_label.setText("Connection failed")
            self.status_label.setStyleSheet("color: red;")
            QMessageBox.critical(self, "Connection Error", message)
    
    def handle_disconnect(self):
        """Handle disconnect"""
        self.db_service.disconnect()
        self.status_label.setText("Not connected")
        self.status_label.setStyleSheet("color: gray;")
        self.connect_btn.setText("Connect")
        self.connect_btn.clicked.disconnect()
        self.connect_btn.clicked.connect(self.handle_connect)
        
        # Clear lists
        self.database_list.clear()
        self.container_list.clear()
        self.current_database = None
    
    def load_databases(self):
        """Load databases from Cosmos DB"""
        databases = self.db_service.get_databases()
        self.database_list.clear()
        self.database_list.addItems(databases)
    
    def handle_database_selected(self, item):
        """Handle database selection"""
        database_name = item.text()
        self.current_database = database_name
        self.database_selected.emit(database_name)
        
        # Load containers for this database
        self.load_containers(database_name)
    
    def load_containers(self, database_name: str):
        """Load containers for a database"""
        containers = self.db_service.get_containers(database_name)
        self.container_list.clear()
        self.container_list.addItems(containers)
    
    def handle_container_selected(self, item):
        """Handle container selection"""
        if self.current_database:
            container_name = item.text()
            self.container_selected.emit(self.current_database, container_name)
    
    def load_saved_connections(self):
        """Load saved connections from storage"""
        self.saved_connections_list.clear()
        connections = self.storage_service.get_all_connections()
        
        for conn_id, name in connections:
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, conn_id)  # Store the ID in the item
            self.saved_connections_list.addItem(item)
    
    def handle_add_connection(self):
        """Handle add connection button click"""
        dialog = ConnectionDialog(self)
        
        if dialog.exec():
            name, config = dialog.get_result()
            
            # Save to storage
            success, message = self.storage_service.save_connection(name, config)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.load_saved_connections()
            else:
                QMessageBox.warning(self, "Error", message)
    
    def handle_remove_connection(self):
        """Handle remove connection button click"""
        current_item = self.saved_connections_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a connection to remove")
            return
        
        connection_name = current_item.text()
        connection_id = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete connection '{connection_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.storage_service.delete_connection(connection_id)
            
            if success:
                QMessageBox.information(self, "Success", message)
                self.load_saved_connections()
            else:
                QMessageBox.warning(self, "Error", message)
