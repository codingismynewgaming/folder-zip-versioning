"""
Test script for the zip versioning logic
"""

import os
import sys
import zipfile
import re
from pathlib import Path

# Add app-files to path
sys.path.insert(0, os.path.dirname(__file__))

def get_next_version_number(folder_path):
    """Find the next available version number for the zip file."""
    parent_dir = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path)
    
    # Pattern to match foldername_XXX.zip (where XXX is 1-3 digits)
    pattern = re.compile(rf'^{re.escape(folder_name)}_(\d{{1,3}})\.zip$', re.IGNORECASE)
    
    existing_versions = []
    
    # Scan parent directory for existing zips
    for item in os.listdir(parent_dir):
        match = pattern.match(item)
        if match:
            version_num = int(match.group(1))
            existing_versions.append(version_num)
    
    # Return next version number
    if existing_versions:
        return max(existing_versions) + 1
    else:
        return 1

def zip_folder(folder_path, version_num):
    """Create a zip file of the folder with version number."""
    parent_dir = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path)
    zip_filename = f"{folder_name}_{version_num:03d}.zip"
    zip_path = os.path.join(parent_dir, zip_filename)
    
    # Create the zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate relative path for the archive
                arcname = os.path.relpath(file_path, parent_dir)
                zipf.write(file_path, arcname)
    
    return zip_path

def test_versioning():
    """Test the auto-versioning logic."""
    test_dir = r"D:\personaldata\vibe-coding-projekte\zip-folder-automation"
    test_folder = os.path.join(test_dir, "test-folder")
    
    print("🧪 Testing auto-versioning logic...\n")
    
    # Test 1: First version (should be 1)
    print("Test 1: Getting first version number...")
    version = get_next_version_number(test_folder)
    assert version == 1, f"Expected 1, got {version}"
    print(f"✓ First version: {version}")
    
    # Test 2: Create first zip
    print("\nTest 2: Creating first zip...")
    zip_path = zip_folder(test_folder, version)
    assert os.path.exists(zip_path), f"Zip file not created: {zip_path}"
    print(f"✓ Created: {os.path.basename(zip_path)}")
    
    # Test 3: Second version (should be 2)
    print("\nTest 3: Getting second version number...")
    version = get_next_version_number(test_folder)
    assert version == 2, f"Expected 2, got {version}"
    print(f"✓ Second version: {version}")
    
    # Test 4: Create second zip
    print("\nTest 4: Creating second zip...")
    zip_path = zip_folder(test_folder, version)
    assert os.path.exists(zip_path), f"Zip file not created: {zip_path}"
    print(f"✓ Created: {os.path.basename(zip_path)}")
    
    # Test 5: Third version (should be 3)
    print("\nTest 5: Getting third version number...")
    version = get_next_version_number(test_folder)
    assert version == 3, f"Expected 3, got {version}"
    print(f"✓ Third version: {version}")
    
    # Verify zip contents
    print("\nTest 6: Verifying zip contents...")
    first_zip = os.path.join(test_dir, "test-folder_001.zip")
    with zipfile.ZipFile(first_zip, 'r') as zipf:
        files = zipf.namelist()
        print(f"✓ Zip contains {len(files)} items:")
        for f in files[:5]:  # Show first 5
            print(f"  - {f}")
    
    print("\n✅ All tests passed!")
    print("\nCreated files:")
    for item in os.listdir(test_dir):
        if item.endswith('.zip'):
            print(f"  📦 {item}")

if __name__ == "__main__":
    test_versioning()
