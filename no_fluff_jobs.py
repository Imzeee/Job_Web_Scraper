from selenium.webdriver import Opera
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re


class BrowserBot:

    def __init__(self):
        self.driver = Opera(executable_path='./operadriver')
        self.driver.get("https://nofluffjobs.com/pl")
        self.driver.fullscreen_window()

        self.jobs_descriptions = []
        self.jobs_links = []

    def click_confirm_button(self):
        try:
            buttons = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "btn")))
            for button in buttons:
                if button.text == "Zatwierdź":
                    button.click()
                    break
        except NoSuchElementException:
            print("Error in click_confirm_button()")
            self.driver.quit()

    def print_job_offers(self):
        print(f"Found {len(self.jobs_links)} jobs")
        for i in range(len(self.jobs_links)):
            print(f"{i + 1} JOB:")
            print(f"{self.jobs_descriptions[i]} {self.jobs_links[i]}")

    def collect_jobs_descriptions(self):
        try:
            headers = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'posting-list-item')))
            for header in headers:
                temp_list = list(header.text.split("\n"))
                self.jobs_descriptions.append(temp_list[0])
        except NoSuchElementException:
            print("Error in collect_jobs_description()")
            self.driver.quit()

    def collect_jobs_links(self):
        try:
            find = self.driver.find_elements_by_xpath('.//a')
            for a in find:
                temp = str(a.get_attribute('href'))
                if re.search("^.*/job/.*$", temp):
                    self.jobs_links.append(a.get_attribute('href'))
        except NoSuchElementException:
            print("Error in collect_jobs_links()")
            self.driver.quit()

    def page_scroll(self, scroll_list):
        pages = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "page-item")))
        checkpoint = False
        for page in pages:

            if checkpoint and (page.text == str(scroll_list[0] + 1)):
                print("Found next")
                scroll_list[1] = True

            if page.text == str(scroll_list[0]):
                print("Clicking")
                try:
                    self.driver.implicitly_wait(1)
                    page.click()
                except NoSuchElementException:
                    print("Error in page_scroll()")
                    self.driver.quit()
                checkpoint = True
                continue

    def scroll_all_pages(self):
        pages_available = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "page-item")))
        check = False
        for pa in pages_available:
            if pa.text == str(2):
                check = True
        scroll_list = [2, False]
        if check:
            while True:
                scroll_list[1] = False
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1500);")
                self.page_scroll(scroll_list)
                self.collect_jobs_descriptions()
                self.collect_jobs_links()
                scroll_list[0] = scroll_list[0] + 1
                if not scroll_list[1]:
                    break

    def find_location_filter(self, name, user_input):
        filters = self.driver.find_elements_by_class_name("d-inline-block")
        for site_filter in filters:
            if site_filter.text == name:
                site_filter.click()
        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "filters-btn")))

            for proper_element in elements:
                if proper_element.text in user_input:
                    proper_element.click()

        except NoSuchElementException:
            print("Error in find_location_filter()")
            self.driver.quit()

    def find_more_button_filter(self, name, user_input):
        filters = self.driver.find_elements_by_class_name("d-inline-block")
        for site_filter in filters:
            if site_filter.text == "Więcej":
                site_filter.click()
        try:
            labels = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "label")))
            for label in labels:
                try:
                    if label.text in user_input:
                        label.click()
                except NoSuchElementException:
                    print("Error in find_more_button_filter()")
                    self.driver.quit()
        except NoSuchElementException:
            print("Error in find_more_button_filter()")
            self.driver.quit()

    def check_level(self, user_input):
        try:
            labels = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "label")))
            for label in labels:
                try:
                    if label.text in user_input:
                        label.click()
                except NoSuchElementException:
                    print("Error while checking seniority")
                    self.driver.quit()
        except NoSuchElementException:
            print("Error while selecting seniority")
            self.driver.quit()

    def close_pop_up(self):
        try:
            element = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "close")))
            element.click()
        except NoSuchElementException:
            print("There is no pop-up")
            pass

    def close_browser(self):
        self.driver.quit()
