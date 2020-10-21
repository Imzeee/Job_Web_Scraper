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
        print(f"FOUND {len(self.jobs_links)} JOBS\n-------------")
        for i in range(len(self.jobs_links)):
            print(f"{i + 1}: {self.jobs_descriptions[i]} \t LINK:{self.jobs_links[i]}")

    def collect_jobs_descriptions(self):
        try:
            headers = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'posting-list-item')))
            for header in headers:
                self.jobs_descriptions.append(list(header.text.split("\n"))[0])
        except NoSuchElementException:
            print("Error in collect_jobs_description()")
            self.driver.quit()

    def collect_jobs_links(self):
        try:
            links = self.driver.find_elements_by_xpath('.//a')
            for link in links:
                if re.search("^.*/job/.*$", str(link.get_attribute('href'))):
                    self.jobs_links.append(link.get_attribute('href'))
        except NoSuchElementException:
            print("Error in collect_jobs_links()")
            self.driver.quit()

    def page_scroll(self, scroll_list):
        pages = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "page-item")))
        checkpoint = False
        for page in pages:
            if checkpoint and (page.text == str(scroll_list[0] + 1)):
                scroll_list[1] = True
            if page.text == str(scroll_list[0]):
                try:
                    self.driver.implicitly_wait(1)
                    page.click()
                except NoSuchElementException:
                    print("Error in page_scroll()")
                    self.driver.quit()
                checkpoint = True
                continue

    def collect_job_offers(self):
        pages_available = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "page-item")))
        check = False
        for pa in pages_available:
            if pa.text == str(2):
                check = True
        scroll_list = [2, False]
        self.collect_jobs_links()
        self.collect_jobs_descriptions()
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

    def choose_location_filters(self, user_input):
        filters = self.driver.find_elements_by_class_name("d-inline-block")
        for site_filter in filters:
            if site_filter.text == "Lokalizacje":
                site_filter.click()
        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "filters-btn")))
            for element in elements:
                if element.text in user_input:
                    element.click()
        except NoSuchElementException:
            print("Error in find_location_filter()")
            self.driver.quit()

    def choose_level_filters(self, user_input):
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
                    print("Error in choose_level_filters()")
                    self.driver.quit()
        except NoSuchElementException:
            print("Error in choose_level_filters()")
            self.driver.quit()

    def choose_category(self, user_input):
        filters = self.driver.find_elements_by_class_name("d-inline-block")
        for site_filter in filters:
            if site_filter.text == "Kategoria":
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

    def close_browser(self):
        self.driver.quit()
