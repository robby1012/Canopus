# Canopus

A PyQt6-based desktop application for browsing Azure Cosmos DB databases and containers.

## History

I created this app for easier & quick solution browsing Azure Cosmos for debugging my microservices, my workplace have complicated SOP just for checking Cosmos data. So what the heck, why not created simple app to make my life easier, right? :)

So that's why I created this app for read only operations, please use official Azure Portal for CRUD operations.

## Features

- **Connection Manager**: Connect to Azure Cosmos DB using endpoint and key
- **Database Navigation**: Browse databases and containers
- **Data Viewer**: View container data in a table format
- **Column Filtering**: Filter data by column values
- **Sorting**: Sort columns in ascending or descending order
- **Full-screen UI**: App runs in maximized window mode

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Click + button, Enter your Azure Cosmos DB OAuth2 credentials:
   - **Connection Name**: Connection profile name (e.g My DB)
   - **Cosmos Endpoint**: Your Cosmos DB account endpoint (e.g., `https://your-account.documents.azure.com:443/`)
   - **Service URL**: Azure AD OAuth endpoint (e.g., `https://login.microsoftonline.com/<tenant-id>`)
   - **Client ID**: Your application (client) ID
   - **Client Secret**: Your client secret value
   - **Resource**: Cosmos DB resource URI (default: `https://cosmos.azure.com`)

3. Click "Connect" to establish connection

4. Browse databases in the sidebar

5. Select a container to view its data

6. Use the filter fields above each column to filter data

7. Click column headers to sort

## Project Structure

```
.
├── main.py                          # Application entry point
├── models/
│   └── connection_config.py         # Connection configuration model
├── services/
│   └── cosmos_storage_service.py    # SQlite DB Service Layer
│   └── cosmos_db_service.py         # Cosmos DB service layer
├── ui/
│   ├── main_window.py               # Main application window
│   ├── sidebar.py                   # Sidebar with connection & navigation
│   └── table_view.py                # Table view with filtering & sorting
├── requirements.txt                 # Python dependencies
```

## Requirements

- Python 3.8+
- PyQt6
- azure-cosmos

## Optional Requirements

- cairosvg
- Pillow
- py2app
