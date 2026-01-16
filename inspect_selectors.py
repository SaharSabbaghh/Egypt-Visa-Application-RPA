"""
Script to inspect the Egypt visa form and find correct selectors
"""

import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def inspect_form():
    """Open the form and inspect all input fields"""
    
    # Setup Chrome
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1920,1080')
    
    project_root = Path(__file__).parent
    chromedriver_path = project_root / 'bin' / 'chromedriver'
    
    service = Service(executable_path=str(chromedriver_path))
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigate to form
        url = "https://dubai.egyptconsulates.org/new-forms/visas.html"
        print(f"Opening {url}...\n")
        driver.get(url)
        time.sleep(3)
        
        print("="*80)
        print("FORM FIELD INSPECTION")
        print("="*80)
        
        # Find all input fields
        print("\n--- INPUT FIELDS ---")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for idx, inp in enumerate(inputs, 1):
            name = inp.get_attribute("name") or ""
            input_id = inp.get_attribute("id") or ""
            input_type = inp.get_attribute("type") or "text"
            placeholder = inp.get_attribute("placeholder") or ""
            input_class = inp.get_attribute("class") or ""
            
            if name or input_id:  # Only show fields with name or id
                print(f"\n{idx}. Type: {input_type:10}")
                if name:
                    print(f"   name=\"{name}\"")
                    print(f"   Selector: input[name='{name}']")
                if input_id:
                    print(f"   id=\"{input_id}\"")
                    print(f"   Selector: #{input_id}")
                if placeholder:
                    print(f"   Placeholder: {placeholder[:50]}")
        
        # Find all textarea fields
        print("\n\n--- TEXTAREA FIELDS ---")
        textareas = driver.find_elements(By.TAG_NAME, "textarea")
        for idx, ta in enumerate(textareas, 1):
            name = ta.get_attribute("name") or ""
            ta_id = ta.get_attribute("id") or ""
            placeholder = ta.get_attribute("placeholder") or ""
            
            if name or ta_id:
                print(f"\n{idx}.")
                if name:
                    print(f"   name=\"{name}\"")
                    print(f"   Selector: textarea[name='{name}']")
                if ta_id:
                    print(f"   id=\"{ta_id}\"")
                    print(f"   Selector: #{ta_id}")
                if placeholder:
                    print(f"   Placeholder: {placeholder[:50]}")
        
        # Find all select dropdowns
        print("\n\n--- SELECT DROPDOWNS ---")
        selects = driver.find_elements(By.TAG_NAME, "select")
        for idx, sel in enumerate(selects, 1):
            name = sel.get_attribute("name") or ""
            sel_id = sel.get_attribute("id") or ""
            options = sel.find_elements(By.TAG_NAME, "option")
            option_texts = [opt.text.strip() for opt in options if opt.text.strip()]
            
            if name or sel_id:
                print(f"\n{idx}.")
                if name:
                    print(f"   name=\"{name}\"")
                    print(f"   Selector: select[name='{name}']")
                if sel_id:
                    print(f"   id=\"{sel_id}\"")
                    print(f"   Selector: #{sel_id}")
                if option_texts:
                    print(f"   Options: {', '.join(option_texts[:3])}...")
        
        # Find all buttons
        print("\n\n--- BUTTONS ---")
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for idx, btn in enumerate(buttons, 1):
            text = btn.text.strip()
            btn_type = btn.get_attribute("type") or "button"
            btn_class = btn.get_attribute("class") or ""
            btn_id = btn.get_attribute("id") or ""
            
            if text or btn_id:
                print(f"\n{idx}. Type: {btn_type}")
                if text:
                    print(f"   Text: {text[:40]}")
                if btn_id:
                    print(f"   id=\"{btn_id}\"")
                if btn_class:
                    print(f"   class=\"{btn_class[:50]}\"")
        
        print("\n" + "="*80)
        print("\nInspection complete! Browser will stay open for 30 seconds...")
        print("You can manually inspect the page if needed.")
        time.sleep(30)
    
    finally:
        driver.quit()

if __name__ == "__main__":
    inspect_form()

