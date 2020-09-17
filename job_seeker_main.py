from selenium.webdriver import Opera
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


def button_confirm():
    try:
        buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "btn")))
        for button in buttons:
            try:
                if button.text == "Zatwierdź":
                    button.click()
                    break
            except:
                pass
    except:
        print("Error while searching for confirm button")
        driver.quit()


def print_jobs(jobs, links):
    print(f"Found {len(links)} jobs")
    for i in range(len(links)):
        print(f"{i+1} JOB:")
        print(f"{jobs[i][0]} {jobs[i][-1]} {links[i]}")


def collect_information(jobs):
    try:
        headers = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'posting-list-item')))
        try:
            for header in headers:
                temp_list = list(header.text.split("\n"))
                jobs.append(temp_list)
        except:
            print("Error while collecting data")
    except:
        print("Error while scraping info")


def collect_links(proper):
    try:
        find = driver.find_elements_by_xpath('.//a')
        for a in find:
            temp = str(a.get_attribute('href'))
            if re.search("^.*/job/.*$", temp):
                proper.append(a.get_attribute('href'))
    except:
        print("Error while scraping links")


def page_scroll(scroll_list):
    print("Scrolling page")
    pages = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "page-item")))
    checkpoint = False
    for page in pages:

        if checkpoint and (page.text == str(scroll_list[0] + 1)):
            print("Found next")
            scroll_list[1] = True

        if page.text == str(scroll_list[0]):
            print("Clicking")
            try:
                page.click()
            except:
                print("Clicking error")
            checkpoint = True
            continue


print("Choose locations by typing names of the cities seperated by spaces")
print("""Avialable options: Warszawa, Wrocław, Kraków, Gdańsk, Poznań, Trójmiasto, Sląśk, Łódź, Katowice 
                Lublin, Szczecin, "Bydgoszcz, Białystko, Gdynia, Gliwice , Sopot""")

input_lokalizacje = list(map(str, input().split()))

print("Choose seniority by typing levels seperated by space")
print("Avialable options: Stażysta, Junior, Mid, Senior, Expert")
input_seniority = list(map(str, input().split()))

print("Wait, collecting data...")

driver = Opera(executable_path='./operadriver')
driver.get("https://nofluffjobs.com/pl")
driver.fullscreen_window()

filters = driver.find_elements_by_class_name("d-inline-block")
for site_filter in filters:
    if site_filter.text == "Lokalizacje":
        site_filter.click()

try:
    elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "filters-btn")))

    for proper_element in elements:
        if proper_element.text in input_lokalizacje:
            proper_element.click()

except:
    print("Error while locating filters buttons")
    driver.quit()


button_confirm()


try:
    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, "close")))
    element.click()

except:
    pass

filters = driver.find_elements_by_class_name("d-inline-block")
for site_filter in filters:
    if site_filter.text == "Więcej":
        site_filter.click()

try:
    labels = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.TAG_NAME, "label")))
    for label in labels:
        try:
            if label.text in input_seniority:
                label.click()
        except:
            pass
except:
    print("Error while selecting seniority")
    driver.quit()

button_confirm()

jobs_information = []
proper_links = []

collect_information(jobs_information)
collect_links(proper_links)
pages_available = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "page-item")))

check = False
for pa in pages_available:
    if pa.text == str(2):
        check = True

if check:
    lst = [2, False]
    while True:
        try:
            lst[1] = False
            print(f"Calling page_scroll num = {lst[0]}")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight - 1500);")
            page_scroll(lst)

            print("Collecting information from page")
            collect_information(jobs_information)

            print("Collecting links from page")
            collect_links(proper_links)

        except:
            pass
        lst[0] = lst[0] + 1
        if not lst[1]:
            break

driver.implicitly_wait(2)
driver.quit()

try:
    print_jobs(jobs_information, proper_links)
except:
    print("Error while printing jobs")




