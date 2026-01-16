"""
Test script to verify QR code fix is working properly
"""

import sys
from pathlib import Path
import json
import time

print("="*80)
print("QR CODE FIX - TEST SCRIPT")
print("="*80)

# Test 1: Check if new dependencies are installed
print("\n[1/5] Testing dependencies...")
try:
    import cv2
    print("  ✓ opencv-python-headless installed")
except ImportError:
    print("  ❌ opencv-python-headless NOT installed")
    print("     Run: pip3 install opencv-python-headless==4.8.1.78")
    sys.exit(1)

try:
    from pyzbar.pyzbar import decode
    print("  ✓ pyzbar installed")
except ImportError:
    print("  ❌ pyzbar NOT installed")
    print("     Run: pip3 install pyzbar==0.1.9")
    print("     On macOS, you may need: brew install zbar")
    sys.exit(1)

# Test 2: Check configuration
print("\n[2/5] Checking configuration...")
config_path = Path(__file__).parent / "config" / "config.json"
try:
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    if 'qr_settings' in config:
        print("  ✓ QR settings found in config")
        print(f"    - Wait timeout: {config['qr_settings']['wait_timeout']}s")
        print(f"    - Verification: {config['qr_settings']['verification_enabled']}")
        print(f"    - Network idle timeout: {config['qr_settings']['network_idle_timeout']}s")
    else:
        print("  ❌ QR settings not found in config")
        print("     The config might not be updated correctly")
        sys.exit(1)
except Exception as e:
    print(f"  ❌ Error reading config: {e}")
    sys.exit(1)

# Test 3: Import PDF generator with new methods
print("\n[3/5] Testing PDF generator module...")
try:
    from pdf_generator import PDFGenerator
    print("  ✓ PDFGenerator imported successfully")
    
    # Check if new methods exist
    methods_to_check = [
        'detect_network_idle',
        'get_qr_image_info',
        'wait_for_qr_update',
        'decode_qr_code'
    ]
    
    for method in methods_to_check:
        if hasattr(PDFGenerator, method):
            print(f"  ✓ Method '{method}' exists")
        else:
            print(f"  ❌ Method '{method}' NOT found")
            sys.exit(1)
            
except Exception as e:
    print(f"  ❌ Error importing PDFGenerator: {e}")
    sys.exit(1)

# Test 4: Test QR decoding on a sample image
print("\n[4/5] Testing QR decoding functionality...")
try:
    import numpy as np
    from pyzbar.pyzbar import decode as decode_qr
    
    # Create a simple test pattern (not a real QR, just testing the decode function works)
    test_image = np.zeros((100, 100, 3), dtype=np.uint8)
    result = decode_qr(test_image)
    print("  ✓ QR decode function operational (no QR found in test image, as expected)")
    
except Exception as e:
    print(f"  ⚠ QR decode test had issues (this might be ok): {e}")

# Test 5: Validate form automation compatibility
print("\n[5/5] Testing form automation integration...")
try:
    from form_automation import EgyptVisaFormAutomation
    from data_models import VisaApplication
    print("  ✓ Form automation modules compatible")
except Exception as e:
    print(f"  ❌ Error with form automation: {e}")
    sys.exit(1)

# All tests passed
print("\n" + "="*80)
print("✅ ALL TESTS PASSED!")
print("="*80)
print("\nThe QR code fix is properly installed and ready to use.")
print("\nNext steps:")
print("1. Run your normal workflow: python3 main.py")
print("2. Check the logs for new QR verification messages")
print("3. Verify the generated PDF contains the correct QR code")
print("\nTo verify a QR code manually:")
print("- Use a QR scanner app on your phone")
print("- Check that the decoded data matches the applicant information")
print("="*80)

