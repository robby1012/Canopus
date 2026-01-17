#!/bin/bash
# Script to create DMG installer for Canopus application

set -e

echo "🚀 Starting DMG creation process..."

# Step 1: Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist

# Step 2: Build the .app bundle
echo "📦 Building .app bundle with py2app..."
./venv/bin/python setup_installer.py py2app

# Step 3: Create DMG
echo "💿 Creating DMG installer..."

APP_NAME="Canopus"
DMG_NAME="Canopus-0.0.1"
APP_PATH="dist/${APP_NAME}.app"
DMG_FINAL="dist/${DMG_NAME}.dmg"

# Remove existing DMG
rm -f "${DMG_FINAL}"

# Create DMG directly
echo "🗜️  Creating compressed DMG..."
hdiutil create -volname "${APP_NAME}" -srcfolder "${APP_PATH}" -ov -format UDZO "${DMG_FINAL}"

echo "✅ DMG created successfully: ${DMG_FINAL}"
echo ""
echo "📍 Location: $(pwd)/${DMG_FINAL}"
echo ""
echo "🎉 Build complete!"
