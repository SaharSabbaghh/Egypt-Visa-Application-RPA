"""
Test using native print dialog
"""
from pathlib import Path
from form_automation import EgyptVisaFormAutomation, VisaFormFiller
from data_models import VisaApplication
from pdf_generator import create_pdf_from_filled_form

# Setup
config_path = Path("config/config.json")
sample_data = Path("data/sample_application.json")

automation = EgyptVisaFormAutomation(config_path)

try:
    automation.setup_driver()
    automation.navigate_to_form()
    
    # Load application
    app = VisaApplication.from_json_file(sample_data)
    
    # Fill form
    filler = VisaFormFiller(automation)
    filler.fill_complete_form(app)
    
    print("\n" + "="*80)
    print("Form filled! Now testing native print dialog method...")
    print("="*80 + "\n")
    
    # Generate PDF using native print dialog
    pdf_path = create_pdf_from_filled_form(automation, app, click_create_button=True)
    
    if pdf_path and pdf_path.exists():
        print(f"\n✅ SUCCESS! PDF created: {pdf_path}")
        print(f"   Size: {pdf_path.stat().st_size / 1024:.1f} KB")
    else:
        print("\n❌ PDF generation failed")
    
finally:
    input("\nPress Enter to close browser...")
    automation.quit()
