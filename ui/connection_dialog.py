"""
Dialog for adding/editing connection configurations
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from models.connection_config import ConnectionConfig


class ConnectionDialog(QDialog):
    """Dialog for adding or editing a connection"""
    
    def __init__(self, parent=None, connection_name: str = "", config: ConnectionConfig = None):
        super().__init__(parent)
        self.connection_name = connection_name
        self.config = config or ConnectionConfig()
        self.result_name = None
        self.result_config = None
        
        self.setup_ui()
        
        # If editing existing connection, populate fields
        if connection_name:
            self.setWindowTitle("Edit Connection")
            self.populate_fields()
        else:
            self.setWindowTitle("Add New Connection")
    
    def setup_ui(self):
        """Setup the UI components"""
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        
        # Connection Name
        name_row = QHBoxLayout()
        name_label = QLabel("Connection Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("My Connection")
        name_row.addWidget(name_label, 1)
        name_row.addWidget(self.name_input, 2)
        layout.addLayout(name_row)
        
        # Cosmos Endpoint
        endpoint_row = QHBoxLayout()
        endpoint_label = QLabel("Cosmos Endpoint:")
        self.cosmos_endpoint_input = QLineEdit()
        self.cosmos_endpoint_input.setPlaceholderText("https://your-account.documents.azure.com:443/")
        endpoint_row.addWidget(endpoint_label, 1)
        endpoint_row.addWidget(self.cosmos_endpoint_input, 2)
        layout.addLayout(endpoint_row)
        
        # Service URL
        service_row = QHBoxLayout()
        service_label = QLabel("Service URL:")
        self.service_url_input = QLineEdit()
        self.service_url_input.setPlaceholderText("https://login.microsoftonline.com/<tenant-id>")
        service_row.addWidget(service_label, 1)
        service_row.addWidget(self.service_url_input, 2)
        layout.addLayout(service_row)
        
        # Client ID
        client_id_row = QHBoxLayout()
        client_id_label = QLabel("Client ID:")
        self.client_id_input = QLineEdit()
        self.client_id_input.setPlaceholderText("Your client ID")
        client_id_row.addWidget(client_id_label, 1)
        client_id_row.addWidget(self.client_id_input, 2)
        layout.addLayout(client_id_row)
        
        # Client Secret
        secret_row = QHBoxLayout()
        secret_label = QLabel("Client Secret:")
        self.client_secret_input = QLineEdit()
        self.client_secret_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.client_secret_input.setPlaceholderText("Your client secret")
        secret_row.addWidget(secret_label, 1)
        secret_row.addWidget(self.client_secret_input, 2)
        layout.addLayout(secret_row)
        
        # Resource
        resource_row = QHBoxLayout()
        resource_label = QLabel("Resource:")
        self.resource_input = QLineEdit()
        self.resource_input.setText("https://cosmos.azure.com")
        resource_row.addWidget(resource_label, 1)
        resource_row.addWidget(self.resource_input, 2)
        layout.addLayout(resource_row)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.handle_save)
        save_btn.setDefault(True)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def populate_fields(self):
        """Populate fields with existing connection data"""
        self.name_input.setText(self.connection_name)
        self.cosmos_endpoint_input.setText(self.config.cosmos_endpoint)
        self.service_url_input.setText(self.config.service_url)
        self.client_id_input.setText(self.config.client_id)
        self.client_secret_input.setText(self.config.client_secret)
        self.resource_input.setText(self.config.resource)
    
    def handle_save(self):
        """Handle save button click"""
        name = self.name_input.text().strip()
        cosmos_endpoint = self.cosmos_endpoint_input.text().strip()
        service_url = self.service_url_input.text().strip()
        client_id = self.client_id_input.text().strip()
        client_secret = self.client_secret_input.text().strip()
        resource = self.resource_input.text().strip()
        
        # Validate inputs
        if not name:
            QMessageBox.warning(self, "Input Error", "Please provide a connection name")
            return
        
        if not all([cosmos_endpoint, service_url, client_id, client_secret, resource]):
            QMessageBox.warning(self, "Input Error", "Please provide all required fields")
            return
        
        # Create config
        self.result_name = name
        self.result_config = ConnectionConfig(
            cosmos_endpoint=cosmos_endpoint,
            service_url=service_url,
            client_id=client_id,
            client_secret=client_secret,
            resource=resource
        )
        
        self.accept()
    
    def get_result(self):
        """Get the result (name, config) tuple"""
        return self.result_name, self.result_config
