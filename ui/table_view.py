"""
Table view component with filtering and sorting
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLineEdit, QHBoxLayout, QHeaderView
)
from PyQt6.QtCore import Qt
from typing import List, Dict, Any


class FilterableTableView(QWidget):
    """Table view with column filters and sorting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_data: List[Dict[str, Any]] = []
        self.filtered_data: List[Dict[str, Any]] = []
        self.column_names: List[str] = []
        self.filter_widgets: List[QLineEdit] = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Filter row container
        self.filter_container = QWidget()
        self.filter_layout = QHBoxLayout(self.filter_container)
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.filter_container)
        
        # Table widget
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        layout.addWidget(self.table)
    
    def load_data(self, data: List[Dict[str, Any]]):
        """
        Load data into the table
        
        Args:
            data: List of dictionaries containing the data
        """
        if not data:
            self.clear_table()
            return
        
        self.original_data = data
        self.filtered_data = data.copy()
        
        # Extract column names from first item
        self.column_names = list(data[0].keys())
        
        # Setup filters
        self.setup_filters()
        
        # Populate table
        self.populate_table()
    
    def setup_filters(self):
        """Setup filter text fields for each column"""
        # Clear existing filters
        while self.filter_layout.count():
            child = self.filter_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.filter_widgets.clear()
        
        # Create filter for each column
        for col_name in self.column_names:
            filter_edit = QLineEdit()
            filter_edit.setPlaceholderText(f"Filter {col_name}...")
            filter_edit.textChanged.connect(self.apply_filters)
            self.filter_widgets.append(filter_edit)
            self.filter_layout.addWidget(filter_edit)
    
    def populate_table(self):
        """Populate table with filtered data"""
        self.table.setSortingEnabled(False)
        
        # Set dimensions
        self.table.setRowCount(len(self.filtered_data))
        self.table.setColumnCount(len(self.column_names))
        self.table.setHorizontalHeaderLabels(self.column_names)
        
        # Fill data
        for row_idx, item in enumerate(self.filtered_data):
            for col_idx, col_name in enumerate(self.column_names):
                value = item.get(col_name, '')
                # Convert value to string for display
                cell_value = str(value) if value is not None else ''
                table_item = QTableWidgetItem(cell_value)
                table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row_idx, col_idx, table_item)
        
        self.table.setSortingEnabled(True)
    
    def apply_filters(self):
        """Apply filters to the data"""
        self.filtered_data = self.original_data.copy()
        
        # Apply each column filter
        for col_idx, filter_widget in enumerate(self.filter_widgets):
            filter_text = filter_widget.text().lower().strip()
            if filter_text:
                col_name = self.column_names[col_idx]
                self.filtered_data = [
                    item for item in self.filtered_data
                    if filter_text in str(item.get(col_name, '')).lower()
                ]
        
        # Repopulate table with filtered data
        self.populate_table()
    
    def clear_table(self):
        """Clear all table data"""
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.original_data = []
        self.filtered_data = []
        self.column_names = []
        
        # Clear filters
        while self.filter_layout.count():
            child = self.filter_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.filter_widgets.clear()
