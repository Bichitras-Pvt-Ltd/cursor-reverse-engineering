import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class CursorBot:
    def __init__(self):
        # Load settings
        script_dir = os.path.dirname(os.path.abspath(__file__))
        settings_path = os.path.join(script_dir, '..', '..', 'config', 'settings.json')
        with open(settings_path) as f:
            self.settings = json.load(f)
        
        # Setup logging
        log_dir = os.path.dirname(self.settings['paths']['logs_file'])
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            filename=self.settings['paths']['logs_file'],
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self.driver = None
        self.setup_browser()

    def setup_browser(self):
        options = Options()
        options.add_argument(f'user-agent={self.settings["browser"]["user_agent"]}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--lang=en-US')
        options.add_argument('--start-maximized')
        
        # Setup Chrome profile
        chrome_profile = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            self.settings['paths']['chrome_profile']
        ))
        os.makedirs(chrome_profile, exist_ok=True)
        options.add_argument(f'user-data-dir={chrome_profile}')
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(
            self.settings['browser']['window_size']['width'],
            self.settings['browser']['window_size']['height']
        )

    def wait_for_manual_verification(self, timeout=None):
        if timeout is None:
            timeout = self.settings['browser']['timeout']
        
        print("Cloudflare verification detected. Please complete the verification manually.")
        logging.info("Waiting for manual Cloudflare verification")
        
        try:
            # Wait for the email input field to appear (indicating verification is complete)
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
            )
            logging.info("Manual verification completed successfully")
        except TimeoutException:
            logging.error(f"Verification timeout after {timeout} seconds")
            raise Exception("Verification timeout - please try again")

    def sign_up_cursor(self):
        try:
            self.driver.get("https://cursor.sh")
            
            # Check for Cloudflare verification
            if "challenge" in self.driver.current_url or "cloudflare" in self.driver.current_url:
                self.wait_for_manual_verification()
            
            # Continue with signup process
            # ... (rest of the signup logic)
            
            # Save account details
            accounts_dir = os.path.dirname(self.settings['paths']['accounts_file'])
            os.makedirs(accounts_dir, exist_ok=True)
            with open(self.settings['paths']['accounts_file'], 'a') as f:
                f.write(f"Email: {email}\nPassword: {self.settings['credentials']['password']}\n\n")
            
            logging.info("Account created successfully")
            
        except Exception as e:
            logging.error(f"Error during signup: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    bot = CursorBot()
    bot.sign_up_cursor() 