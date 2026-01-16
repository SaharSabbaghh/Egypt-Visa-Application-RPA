"""
Automated debug to understand QR code generation
"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def debug_qr():
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    
    project_root = Path(__file__).parent
    chromedriver_path = project_root / 'bin' / 'chromedriver'
    service = Service(executable_path=str(chromedriver_path))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("Opening form...")
        driver.get("https://dubai.egyptconsulates.org/new-forms/visas.html")
        time.sleep(3)
        
        # Fill minimal data
        print("Filling minimal form data...")
        driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Test")
        driver.find_element(By.CSS_SELECTOR, "input[name='arName']").send_keys("User")
        driver.find_element(By.CSS_SELECTOR, "input[name='title']").send_keys("Debug")
        
        print("Before clicking submit button...")
        driver.save_screenshot("screenshots/debug_before_submit.png")
        
        # Get page URL before submission
        url_before = driver.current_url
        print(f"URL before: {url_before}")
        
        # Click submit button
        print("\nClicking submit button...")
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'أنشاء و طباعة النموذج')]")
        submit_button.click()
        
        # Immediately after click
        time.sleep(2)
        url_after_2sec = driver.current_url
        print(f"URL after 2sec: {url_after_2sec}")
        driver.save_screenshot("screenshots/debug_after_2sec.png")
        
        # After 5 seconds
        time.sleep(3)
        url_after_5sec = driver.current_url
        print(f"URL after 5sec: {url_after_5sec}")
        driver.save_screenshot("screenshots/debug_after_5sec.png")
        
        # After 10 seconds
        time.sleep(5)
        url_after_10sec = driver.current_url
        print(f"URL after 10sec: {url_after_10sec}")
        driver.save_screenshot("screenshots/debug_after_10sec.png")
        
        # After 15 seconds
        time.sleep(5)
        url_after_15sec = driver.current_url
        print(f"URL after 15sec: {url_after_15sec}")
        driver.save_screenshot("screenshots/debug_after_15sec.png")
        
        # Check for new elements
        print("\n" + "="*80)
        print("ANALYSIS")
        print("="*80)
        
        # Check if URL changed (redirect happened)
        if url_before != url_after_15sec:
            print(f"✓ URL CHANGED!")
            print(f"  From: {url_before}")
            print(f"  To: {url_after_15sec}")
        else:
            print("✗ URL stayed the same")
        
        # Look for specific elements
        try:
            # Check for modal/popup
            modals = driver.find_elements(By.CSS_SELECTOR, ".modal, [role='dialog']")
            print(f"\nModals/Dialogs found: {len(modals)}")
            
            # Check for print button
            print_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'طباعة') or contains(text(), 'Print')]")
            print(f"Print buttons found: {len(print_buttons)}")
            
            # Check all visible elements with QR in them
            all_elements = driver.find_elements(By.XPATH, "//*")
            qr_related = []
            for elem in all_elements:
                try:
                    if elem.is_displayed():
                        classes = elem.get_attribute('class') or ''
                        ids = elem.get_attribute('id') or ''
                        if 'qr' in classes.lower() or 'qr' in ids.lower():
                            qr_related.append(elem)
                except:
                    pass
            print(f"QR-related visible elements: {len(qr_related)}")
            
            # Check for canvas (QR often rendered on canvas)
            canvases = driver.find_elements(By.TAG_NAME, "canvas")
            visible_canvases = [c for c in canvases if c.is_displayed()]
            print(f"Visible canvas elements: {len(visible_canvases)}")
            
            # Check page title
            print(f"\nPage title: {driver.title}")
            
            # Check if there's a print preview
            page_source = driver.page_source
            if 'application/pdf' in page_source:
                print("✓ PDF detected in page")
            
        except Exception as e:
            print(f"Error during analysis: {e}")
        
        print("\n" + "="*80)
        print("Browser will stay open for 30 seconds for manual inspection...")
        print("="*80)
        time.sleep(30)
        
    finally:
        driver.quit()
        print("\nDebug complete! Check screenshots folder.")

if __name__ == "__main__":
    debug_qr()

