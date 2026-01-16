"""
Debug script to understand the form submission and QR code generation
"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def debug_form_submission():
    """Watch what happens when we submit the form"""
    
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    
    project_root = Path(__file__).parent
    chromedriver_path = project_root / 'bin' / 'chromedriver'
    
    service = Service(executable_path=str(chromedriver_path))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        url = "https://dubai.egyptconsulates.org/new-forms/visas.html"
        print(f"Opening {url}...")
        driver.get(url)
        time.sleep(3)
        
        print("\n" + "="*80)
        print("WAITING FOR YOU TO MANUALLY FILL A SIMPLE FORM")
        print("="*80)
        print("\nPlease:")
        print("1. Fill in just a few basic fields (name, etc.)")
        print("2. Click the 'أنشاء و طباعة النموذج' button")
        print("3. Watch what happens")
        print("\nI'll take screenshots at different stages...")
        
        input("\nPress Enter when you've clicked the submit button...")
        
        # Take screenshot right after submission
        driver.save_screenshot("screenshots/debug_after_submit.png")
        print("✓ Screenshot 1 saved: after submit button clicked")
        
        print("\nWaiting 5 seconds...")
        time.sleep(5)
        driver.save_screenshot("screenshots/debug_after_5sec.png")
        print("✓ Screenshot 2 saved: 5 seconds after submit")
        
        print("\nWaiting another 10 seconds...")
        time.sleep(10)
        driver.save_screenshot("screenshots/debug_after_15sec.png")
        print("✓ Screenshot 3 saved: 15 seconds after submit")
        
        # Check current URL
        current_url = driver.current_url
        print(f"\nCurrent URL: {current_url}")
        
        # Check for iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"Number of iframes: {len(iframes)}")
        
        # Check for any new windows/tabs
        windows = driver.window_handles
        print(f"Number of windows/tabs: {len(windows)}")
        
        # Look for print-related elements
        print("\nLooking for print/QR related elements...")
        
        # Check page source for QR
        page_source = driver.page_source
        if 'qr' in page_source.lower() or 'QR' in page_source:
            print("✓ Found 'QR' in page source")
        else:
            print("✗ No 'QR' found in page source")
        
        # Look for canvas elements (QR codes often rendered on canvas)
        canvases = driver.find_elements(By.TAG_NAME, "canvas")
        print(f"Canvas elements found: {len(canvases)}")
        
        # Look for images
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"Image elements found: {len(images)}")
        for idx, img in enumerate(images[:5]):  # Show first 5
            src = img.get_attribute('src') or ''
            alt = img.get_attribute('alt') or ''
            if src or alt:
                print(f"  Image {idx+1}: src={src[:50]}... alt={alt}")
        
        # Check for print dialog or new content
        print("\nChecking for print-related content...")
        try:
            print_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'print') or contains(text(), 'Print') or contains(text(), 'طباعة')]")
            print(f"Print-related elements: {len(print_elements)}")
        except:
            pass
        
        print("\n" + "="*80)
        print("Debug complete! Check the screenshots to see what happened.")
        print("="*80)
        
        input("\nPress Enter to close browser...")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_form_submission()

