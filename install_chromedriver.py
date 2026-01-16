#!/usr/bin/env python3
"""
Helper script to download and install ChromeDriver for the project
"""

import os
import sys
import zipfile
import urllib.request
import platform
from pathlib import Path

# Determine the correct ChromeDriver version and architecture
CHROMEDRIVER_VERSION = "131.0.6778.87"  # Compatible with most Chrome versions

def get_platform_info():
    """Determine the platform and architecture"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == 'darwin':
        if 'arm' in machine or machine == 'aarch64':
            return 'mac-arm64'
        else:
            return 'mac-x64'
    elif system == 'linux':
        return 'linux64'
    elif system == 'windows':
        return 'win64'
    else:
        raise Exception(f"Unsupported platform: {system}")

def download_chromedriver():
    """Download and install ChromeDriver"""
    print("="*60)
    print("ChromeDriver Installer for Egypt Visa Form RPA")
    print("="*60)
    
    # Get platform
    try:
        platform_name = get_platform_info()
        print(f"\n✓ Detected platform: {platform_name}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False
    
    # Setup paths
    project_root = Path(__file__).parent
    bin_dir = project_root / 'bin'
    bin_dir.mkdir(exist_ok=True)
    
    chromedriver_path = bin_dir / ('chromedriver.exe' if 'win' in platform_name else 'chromedriver')
    
    # Check if already installed
    if chromedriver_path.exists():
        print(f"\n⚠ ChromeDriver already exists at: {chromedriver_path}")
        response = input("  Reinstall? (y/n): ").lower()
        if response != 'y':
            print("Installation cancelled.")
            return True
        chromedriver_path.unlink()
    
    # Download URL
    url = f"https://storage.googleapis.com/chrome-for-testing-public/{CHROMEDRIVER_VERSION}/{platform_name}/chromedriver-{platform_name}.zip"
    
    print(f"\n📥 Downloading ChromeDriver...")
    print(f"   URL: {url}")
    
    zip_path = bin_dir / 'chromedriver.zip'
    
    try:
        # Download with progress
        def reporthook(count, block_size, total_size):
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write(f"\r   Progress: {percent}%")
            sys.stdout.flush()
        
        urllib.request.urlretrieve(url, zip_path, reporthook)
        print("\n✓ Download complete")
        
    except Exception as e:
        print(f"\n✗ Download failed: {e}")
        print("\nPlease download manually from:")
        print(f"  {url}")
        print(f"\nThen extract chromedriver to: {chromedriver_path}")
        return False
    
    # Extract
    print("\n📦 Extracting...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Find chromedriver in the zip
            for file in zip_ref.namelist():
                if file.endswith('chromedriver') or file.endswith('chromedriver.exe'):
                    # Extract just the chromedriver binary
                    source = zip_ref.open(file)
                    target = open(chromedriver_path, 'wb')
                    with source, target:
                        target.write(source.read())
                    break
        
        zip_path.unlink()  # Remove zip file
        print(f"✓ Extracted to: {chromedriver_path}")
        
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        return False
    
    # Make executable (Unix-like systems)
    if platform.system().lower() != 'windows':
        print("\n🔧 Making executable...")
        os.chmod(chromedriver_path, 0o755)
        
        # Try to remove quarantine attribute on macOS
        if platform.system().lower() == 'darwin':
            try:
                os.system(f'xattr -d com.apple.quarantine "{chromedriver_path}" 2>/dev/null')
                print("✓ Removed macOS quarantine attribute")
            except:
                print("⚠ Could not remove quarantine attribute (may need to do manually)")
    
    # Verify installation
    print("\n🔍 Verifying installation...")
    if chromedriver_path.exists():
        print(f"✓ ChromeDriver installed successfully!")
        print(f"   Location: {chromedriver_path}")
        
        # Try to run it
        try:
            import subprocess
            result = subprocess.run([str(chromedriver_path), '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   Version: {result.stdout.strip()}")
            else:
                print("   Note: May need to approve in System Preferences > Security & Privacy")
        except Exception:
            print("   Note: First run may require system approval")
        
        return True
    else:
        print("✗ Installation failed")
        return False

def main():
    print("\n")
    success = download_chromedriver()
    
    if success:
        print("\n" + "="*60)
        print("✅ Installation Complete!")
        print("="*60)
        print("\nYou can now run the automation:")
        print("  python3 main.py")
        print("\n")
        return 0
    else:
        print("\n" + "="*60)
        print("❌ Installation Failed")
        print("="*60)
        print("\nPlease see SETUP_INSTRUCTIONS.md for manual installation steps.")
        print("\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())

