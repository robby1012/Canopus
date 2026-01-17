"""
py2app setup script for Canopus application.
"""
from setuptools import setup
import os
import sys

# Verify PyQt6 is available, else exit with error
try:
    import PyQt6
    print(f"Found PyQt6 at: {PyQt6.__file__}")
except ImportError:
    print("ERROR: PyQt6 not found in current environment!")
    print("Please activate your virtual environment first:")
    print("  source venv/bin/activate")
    sys.exit(1)

APP = ['main.py']
DATA_FILES = [
    ('', ['models']),
    ('', ['services']),
    ('', ['ui']),
]
OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'requests',
        'certifi',
        'msal',
        'cryptography',
        'chardet',
        'charset_normalizer',
        'urllib3',
        'idna',
        'sqlite3',
        'models',
        'services',
        'ui',
    ],
    'includes': [
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.sip',
    ],
    'site_packages': True,
    'strip': True,  # Strip symbols - helps reduce app size, for development set to False for easier debugging
    'optimize': 2,
    'excludes': [
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'IPython',
    ],
    'iconfile': 'Canopus.icns',
    'plist': {
        'CFBundleName': 'Canopus',
        'CFBundleDisplayName': 'Canopus',
        'CFBundleGetInfoString': 'Canopus - Azure Cosmos DB Browser',
        'CFBundleIdentifier': 'com.rbydev.canopus',
        'CFBundleVersion': '0.0.1',
        'CFBundleShortVersionString': '0.0.1',
        'NSHumanReadableCopyright': 'Copyright © 2026 Robby Sitanala',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '11.0',
    }
}

setup(
    name='Canopus',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
