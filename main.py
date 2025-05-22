
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import time
import os
from dotenv import load_dotenv

load_dotenv()

insta_phone = os.getenv("INSTA_PHONE")
insta_password = os.getenv("INSTA_PASSWORD")
insta_acc = "5.min.crafts"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)



class InstaFollower:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')
        try:
            # Dismiss cookies popup if it appears
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept All']"))
            ).click()
        except:
            pass  # No popup

        username = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password = self.driver.find_element(By.NAME, 'password')
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

        username.send_keys(insta_phone)
        password.send_keys(insta_password)
        login_button.click()

            
        not_now_login_info = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Not now')]"))
        )
        not_now_login_info.click()

        
        
    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{insta_acc}/")

        # Wait until the Followers link is clickable
        followers_btn = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/followers')]"))
        )
        followers_btn.click()

        try:
            # Wait for the modal to be present
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='dialog']")
                )
            )
        except Exception as e:
            print("❌ Modal did not appear: ", e)
            return

        # Scroll the modal to load more users
        for _ in range(30):
            try:
                # Re-find the scrollable container on each loop to avoid stale reference
                modal = self.driver.find_element(
                    By.XPATH,
                    "//div[@role='dialog']//div[contains(@style, 'overflow: auto')]"
                )
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollHeight", modal
                )
                time.sleep(2)
            except Exception as scroll_err:
                print(f"⚠️ Scroll failed: {scroll_err}")
                break

        

    def follow(self):
        # Check and update the (CSS) Selector for the "Follow" buttons as required. 
        all_buttons = self.driver.find_elements(By.CSS_SELECTOR, value='. _acan _acap _acas _aj1- _ap30')

        for button in all_buttons:
            try:
                button.click()
                time.sleep(1.1)
            # Clicking button for someone who is already being followed will trigger dialog to Unfollow/Cancel
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Cancel')]")
                cancel_button.click()

insta = InstaFollower()
insta.login()
insta.find_followers()
insta.follow()
