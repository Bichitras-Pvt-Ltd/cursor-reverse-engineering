import os
import time
import random
import string
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import json

class CursorBot:
    def __init__(self):
        self.mail_tm_api = "https://api.mail.tm"
        self.cursor_url = "https://cursor.sh"
        self.email = None
        self.password = "Bichitras123!!"
        self.first_name = "Bichitras"
        self.last_name = "Pvt. LTD"
        self.token = None
        self.driver = None

    def generate_unique_username(self):
        """Generate a unique username for email"""
        timestamp = str(int(time.time()))[-2:]  # Last 6 digits of timestamp
        random_str = ''.join(random.choices(string.ascii_lowercase, k=2))
        return f"{self.first_name.lower()}_{random_str}{timestamp}"

    def create_email_account(self):
        """Create a new email account using Mail.tm API"""
        try:
            # Get available domains
            domains_response = requests.get(f"{self.mail_tm_api}/domains")
            if domains_response.status_code != 200:
                print(f"Failed to get domains. Status code: {domains_response.status_code}")
                print(f"Response: {domains_response.text}")
                raise Exception("Failed to get mail.tm domains")
            
            domain = domains_response.json()["hydra:member"][0]["domain"]
            
            # Generate unique username
            username = self.generate_unique_username()
            self.email = f"{username}@{domain}"

            # Create account
            account_data = {
                "address": self.email,
                "password": self.password
            }
            
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            response = requests.post(
                f"{self.mail_tm_api}/accounts",
                headers=headers,
                json=account_data
            )
            
            if response.status_code != 201:
                print(f"Failed to create account. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                raise Exception("Failed to create email account")

            # Get authentication token
            auth_data = {
                "address": self.email,
                "password": self.password
            }
            auth_response = requests.post(
                f"{self.mail_tm_api}/token",
                headers=headers,
                json=auth_data
            )
            
            if auth_response.status_code != 200:
                print(f"Failed to get token. Status code: {auth_response.status_code}")
                print(f"Response: {auth_response.text}")
                raise Exception("Failed to get authentication token")
                
            self.token = auth_response.json()["token"]
            print(f"Created email account: {self.email}")

        except requests.exceptions.RequestException as e:
            print(f"Network error occurred: {str(e)}")
            raise Exception("Network error during email account creation")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON response: {str(e)}")
            raise Exception("Invalid API response format")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            raise

    def get_verification_link(self, max_attempts=10, delay=5):
        """Get verification link from email"""
        headers = {"Authorization": f"Bearer {self.token}"}
        
        for _ in range(max_attempts):
            # Get messages
            response = requests.get(f"{self.mail_tm_api}/messages", headers=headers)
            messages = response.json()["hydra:member"]
            
            if messages:
                # Get the first message
                message_id = messages[0]["id"]
                message_response = requests.get(f"{self.mail_tm_api}/messages/{message_id}", headers=headers)
                message_content = message_response.json()
                
                # Extract verification link (you might need to adjust this based on the actual email content)
                # This is a placeholder - you'll need to parse the actual email content
                if "verify" in message_content["text"].lower():
                    verification_link = message_content["text"].split("Click here to verify: ")[1].split()[0]
                    return verification_link
            
            time.sleep(delay)
        
        raise Exception("Verification email not received")

    def setup_browser(self):
        """Setup Selenium WebDriver using undetected-chromedriver"""
        try:
            options = uc.ChromeOptions()
            
            # Create a custom Chrome profile directory
            chrome_profile = os.path.join(os.getcwd(), "chrome_profile")
            os.makedirs(chrome_profile, exist_ok=True)
            options.add_argument(f'--user-data-dir={chrome_profile}')
            options.add_argument('--profile-directory=Default')
            
            # Add user agent
            options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36')
            
            # Add basic arguments
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--disable-extensions')
            
            # Initialize undetected-chromedriver
            self.driver = uc.Chrome(
                options=options,
                driver_executable_path=None,
                headless=False,
                use_subprocess=True,
                suppress_welcome=True
            )
            
            # Execute stealth script
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            # Set page load timeout
            self.driver.set_page_load_timeout(30)
            print("Chrome WebDriver setup successful!")
            
        except Exception as e:
            print(f"Error setting up Chrome WebDriver: {str(e)}")
            raise e

    def save_debug_info(self, message, page_source=None):
        """Save debug information to a file"""
        with open('debug_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Message: {message}\n")
            if self.driver:
                f.write(f"Current URL: {self.driver.current_url}\n")
                try:
                    inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    f.write("\nAll input fields found:\n")
                    for inp in inputs:
                        f.write(f"Input: id={inp.get_attribute('id')}, "
                               f"name={inp.get_attribute('name')}, "
                               f"type={inp.get_attribute('type')}, "
                               f"placeholder={inp.get_attribute('placeholder')}\n")
                except Exception as e:
                    f.write(f"Error getting input fields: {str(e)}\n")
                
                if page_source:
                    f.write("\nPage source:\n")
                    f.write(page_source)
            f.write(f"\n{'='*50}\n")

    def wait_for_manual_verification(self, timeout=120):
        """Wait for manual Cloudflare verification"""
        print("\n=== MANUAL VERIFICATION REQUIRED ===")
        print("Please complete the Cloudflare verification in the browser.")
        print("1. Click the checkbox for 'I'm not a robot'")
        print("2. Complete any additional verification if required")
        print("3. Wait for the verification to complete")
        print("You have 2 minutes to complete the verification.")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                # Check for Turnstile iframe
                iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                turnstile_present = any("turnstile" in iframe.get_attribute("src").lower() for iframe in iframes)
                
                if turnstile_present:
                    # Switch to Turnstile iframe
                    for iframe in iframes:
                        if "turnstile" in iframe.get_attribute("src").lower():
                            self.driver.switch_to.frame(iframe)
                            try:
                                # Try to find and click the checkbox
                                checkbox = WebDriverWait(self.driver, 5).until(
                                    EC.element_to_be_clickable((By.CLASS_NAME, "cf-turnstile"))
                                )
                                checkbox.click()
                                print("Clicked verification checkbox...")
                            except:
                                pass  # Checkbox might already be clicked
                            finally:
                                self.driver.switch_to.default_content()
                
                # Check if verification is complete by looking for email field
                email_input = self.driver.find_element(By.NAME, "email")
                print("Verification completed successfully!")
                time.sleep(2)  # Wait a bit after verification
                return True
            except:
                time.sleep(1)  # Check every second
                continue
        
        raise Exception("Verification timeout - please run the script again")

    def sign_up_cursor(self):
        """Sign up for Cursor"""
        try:
            if not self.driver:
                self.setup_browser()

            print("Navigating directly to Cursor signup page...")
            self.driver.get("https://authenticator.cursor.sh/sign-up")
            time.sleep(5)  # Increased wait time

            # Check for and handle Cloudflare verification
            try:
                # Try to find email input field
                email_input = self.driver.find_element(By.NAME, "email")
            except:
                print("Cloudflare verification detected...")
                self.wait_for_manual_verification()
                # After verification, refresh the page
                self.driver.refresh()
                time.sleep(3)

            print("Filling in registration form...")
            # Fill in email
            email_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(self.email)
            time.sleep(2)

            # Fill in first name using the correct name attribute
            first_name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "first_name"))
            )
            first_name_input.clear()
            first_name_input.send_keys(self.first_name)
            time.sleep(2)

            # Fill in last name using the correct name attribute
            last_name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "last_name"))
            )
            last_name_input.clear()
            last_name_input.send_keys(self.last_name)
            time.sleep(2)

            print("Clicking Continue button...")
            # Try different ways to find the Continue button
            try:
                continue_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue']"))
                )
            except:
                try:
                    continue_button = self.driver.find_element(By.CSS_SELECTOR, "button.continue-button")
                except:
                    try:
                        continue_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'continue')]")
                    except:
                        # If all else fails, try to find any button with 'Continue' text
                        buttons = self.driver.find_elements(By.TAG_NAME, "button")
                        continue_button = None
                        for button in buttons:
                            if 'Continue' in button.text:
                                continue_button = button
                                break
                        if not continue_button:
                            raise Exception("Could not find Continue button")

            # Scroll the button into view and click it
            self.driver.execute_script("arguments[0].scrollIntoView(true);", continue_button)
            time.sleep(1)
            continue_button.click()
            time.sleep(3)

            # Now handle the password page
            print("Filling in password...")
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(self.password)
            time.sleep(2)

            print("Submitting final form...")
            # Try to find the final submit button
            try:
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign up')]"))
                )
            except:
                try:
                    submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Create account')]")
                except:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

            submit_button.click()
            time.sleep(5)  # Wait for submission to complete

            print("Waiting for verification email...")
            verification_link = self.get_verification_link()
            print(f"Got verification link: {verification_link}")
            
            print("Verifying email...")
            self.driver.get(verification_link)
            time.sleep(5)  # Wait for verification to complete

            print("Successfully signed up for Cursor!")
            print(f"Email: {self.email}")
            print(f"Password: {self.password}")

        except Exception as e:
            print(f"Detailed error during sign up: {str(e)}")
            if self.driver:
                try:
                    # Take a screenshot if there's an error
                    self.driver.save_screenshot("error_screenshot.png")
                    print("Error screenshot saved as error_screenshot.png")
                except:
                    pass
            self.save_debug_info(f"Error occurred: {str(e)}", self.driver.page_source if self.driver else None)
            raise e

    def sign_in_cursor(self):
        """Sign in to Cursor"""
        try:
            print("Navigating to Cursor login page...")
            self.driver.get("https://authenticator.cursor.sh/sign-in")
            time.sleep(5)

            # Check for and handle Cloudflare verification
            try:
                # Try to find email input field
                email_input = self.driver.find_element(By.NAME, "email")
            except:
                print("Cloudflare verification detected...")
                self.wait_for_manual_verification()

            print("Filling in login form...")
            # Fill in email
            email_input = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(self.email)
            time.sleep(2)

            # Fill in password
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(self.password)
            time.sleep(2)

            print("Submitting login form...")
            # Try different ways to find the submit button
            try:
                submit_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
                )
            except:
                try:
                    submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
                except:
                    submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log in')]")
            
            submit_button.click()
            time.sleep(5)  # Wait for login to complete

            print("Successfully logged in to Cursor!")
            print(f"Email: {self.email}")

        except Exception as e:
            print(f"Detailed error during sign in: {str(e)}")
            self.save_debug_info(f"Error occurred during sign in: {str(e)}", self.driver.page_source if self.driver else None)
            raise e

    def save_credentials(self):
        """Save account credentials to a file"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"cursor_accounts.txt"
        
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Account Created: {timestamp}\n")
                f.write(f"Temp Mail Account:\n")
                f.write(f"Email: {self.email}\n")
                f.write(f"Password: {self.password}\n")
                f.write(f"Mail.tm Token: {self.token}\n")
                f.write(f"\nCursor Account:\n")
                f.write(f"Email: {self.email}\n")
                f.write(f"Password: {self.password}\n")
                f.write(f"First Name: {self.first_name}\n")
                f.write(f"Last Name: {self.last_name}\n")
                f.write(f"{'='*50}\n")
            print(f"\nCredentials saved to {filename}")
        except Exception as e:
            print(f"Error saving credentials: {str(e)}")

    def cleanup(self):
        """Clean up browser resources"""
        if self.driver:
            try:
                # Close all windows
                for handle in self.driver.window_handles:
                    self.driver.switch_to.window(handle)
                    self.driver.close()
            except:
                pass
            
            try:
                # Quit the driver
                self.driver.quit()
            except:
                pass
            
            # Set driver to None
            self.driver = None

def main():
    bot = CursorBot()
    try:
        # First create email and sign up
        bot.create_email_account()
        
        # Save credentials after email creation
        bot.save_credentials()
        
        bot.sign_up_cursor()
        time.sleep(3)  # Wait between signup and signin
        
        # Then sign in
        print("\nProceeding to sign in...")
        bot.sign_in_cursor()
        
    except Exception as e:
        print(f"Bot failed: {str(e)}")
    finally:
        # Use the cleanup method instead of directly quitting
        bot.cleanup()

if __name__ == "__main__":
    main() 