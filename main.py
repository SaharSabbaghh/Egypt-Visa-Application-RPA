"""
Main entry point for Egypt Visa Form RPA automation
Batch processes multiple visa applications
"""

import sys
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

from data_models import VisaApplication, load_applications_from_directory
from form_automation import EgyptVisaFormAutomation, VisaFormFiller
from pdf_generator import create_pdf_from_filled_form


class BatchProcessor:
    """Batch process multiple visa applications"""
    
    def __init__(self, config_path: Path, data_dir: Path):
        self.config_path = config_path
        self.data_dir = data_dir
        self.logger = self._setup_logger()
        
        # Track results
        self.results = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'applications': []
        }
    
    def _setup_logger(self) -> logging.Logger:
        """Setup batch processor logger"""
        logger = logging.getLogger('BatchProcessor')
        logger.setLevel(logging.INFO)
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_handler = logging.FileHandler(
            log_dir / f'batch_{timestamp}.log',
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def load_applications(self) -> List[VisaApplication]:
        """Load all visa applications from data directory"""
        self.logger.info(f"Loading applications from {self.data_dir}")
        applications = load_applications_from_directory(self.data_dir)
        self.logger.info(f"Found {len(applications)} application(s)")
        return applications
    
    def validate_application(self, app: VisaApplication) -> Tuple[bool, List[str]]:
        """Validate a single application"""
        return app.validate()
    
    def process_single_application(
        self,
        app: VisaApplication,
        automation: EgyptVisaFormAutomation,
        filler: VisaFormFiller
    ) -> dict:
        """
        Process a single visa application
        
        Returns:
            dict with processing result
        """
        app_result = {
            'name': f"{app.first_name} {app.family_name}",
            'success': False,
            'pdf_path': None,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            self.logger.info(f"\n{'='*60}")
            self.logger.info(f"Processing: {app_result['name']}")
            self.logger.info(f"{'='*60}")
            
            # Validate application
            is_valid, errors = self.validate_application(app)
            if not is_valid:
                error_msg = "Validation failed: " + "; ".join(errors)
                self.logger.error(error_msg)
                app_result['error'] = error_msg
                return app_result
            
            self.logger.info("✓ Application validated")
            
            # Navigate to form
            automation.navigate_to_form()
            time.sleep(2)
            
            # Fill the form
            self.logger.info("Filling form...")
            filler.fill_complete_form(app)
            self.logger.info("✓ Form filled")
            
            # Take screenshot before PDF generation
            automation.take_screenshot(f"before_pdf_{app.first_name}_{app.family_name}")
            
            # Generate PDF
            self.logger.info("Generating PDF...")
            pdf_path = create_pdf_from_filled_form(automation, app, click_create_button=True)
            
            if pdf_path and pdf_path.exists():
                self.logger.info(f"✓ PDF saved: {pdf_path}")
                app_result['success'] = True
                app_result['pdf_path'] = str(pdf_path)
            else:
                error_msg = "PDF generation failed"
                self.logger.error(error_msg)
                app_result['error'] = error_msg
            
        except Exception as e:
            error_msg = f"Error processing application: {str(e)}"
            self.logger.error(error_msg, exc_info=True)
            app_result['error'] = error_msg
            
            # Take error screenshot
            try:
                automation.take_screenshot(f"error_{app.first_name}_{app.family_name}")
            except:
                pass
        
        return app_result
    
    def process_all_applications(self):
        """Process all applications in batch mode"""
        self.logger.info("\n" + "="*60)
        self.logger.info("EGYPT VISA FORM BATCH PROCESSOR")
        self.logger.info("="*60 + "\n")
        
        # Load applications
        applications = self.load_applications()
        
        if not applications:
            self.logger.warning("No applications found to process")
            return
        
        self.results['total'] = len(applications)
        
        # Initialize automation
        automation = EgyptVisaFormAutomation(self.config_path)
        
        try:
            # Setup browser
            automation.setup_driver()
            filler = VisaFormFiller(automation)
            
            # Process each application
            for idx, app in enumerate(applications, 1):
                self.logger.info(f"\nProcessing application {idx}/{len(applications)}")
                
                result = self.process_single_application(app, automation, filler)
                self.results['applications'].append(result)
                
                if result['success']:
                    self.results['successful'] += 1
                else:
                    self.results['failed'] += 1
                
                # Add delay between applications
                if idx < len(applications):
                    self.logger.info("Waiting before next application...")
                    time.sleep(3)
        
        finally:
            # Cleanup
            automation.quit()
        
        # Print summary
        self.print_summary()
        self.save_summary_report()
    
    def print_summary(self):
        """Print batch processing summary"""
        self.logger.info("\n" + "="*60)
        self.logger.info("BATCH PROCESSING SUMMARY")
        self.logger.info("="*60)
        self.logger.info(f"Total applications: {self.results['total']}")
        self.logger.info(f"Successful: {self.results['successful']}")
        self.logger.info(f"Failed: {self.results['failed']}")
        self.logger.info("="*60)
        
        if self.results['successful'] > 0:
            self.logger.info("\nSuccessful applications:")
            for app in self.results['applications']:
                if app['success']:
                    self.logger.info(f"  ✓ {app['name']} -> {app['pdf_path']}")
        
        if self.results['failed'] > 0:
            self.logger.info("\nFailed applications:")
            for app in self.results['applications']:
                if not app['success']:
                    self.logger.info(f"  ✗ {app['name']}: {app['error']}")
        
        self.logger.info("\n" + "="*60 + "\n")
    
    def save_summary_report(self):
        """Save summary report to file"""
        import json
        
        log_dir = Path('logs')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = log_dir / f'summary_{timestamp}.json'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Summary report saved: {report_path}")


def main():
    """Main entry point"""
    # Paths
    config_path = Path(__file__).parent / "config" / "config.json"
    data_dir = Path(__file__).parent / "data"
    
    # Check if config exists
    if not config_path.exists():
        print(f"Error: Config file not found at {config_path}")
        sys.exit(1)
    
    # Check if data directory exists
    if not data_dir.exists():
        print(f"Error: Data directory not found at {data_dir}")
        sys.exit(1)
    
    # Create and run batch processor
    processor = BatchProcessor(config_path, data_dir)
    
    try:
        processor.process_all_applications()
    except KeyboardInterrupt:
        print("\n\nBatch processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

