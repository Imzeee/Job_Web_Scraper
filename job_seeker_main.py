import no_fluff_jobs
from tabulate import tabulate

cities = [["Warszawa", "Wrocław", "Kraków", "Gdańsk"], ["Poznań", "Trójmiasto", "Śląsk", "Łódź"],
                  ["Katowice", "Lublin", "Szczecin", "Bydgoszcz"], ["Białystok", "Gdynia", "Gliwice", "Sopot"]]

categories = [["Backend", "Frontend", "Fullstack", "Mobile"], ["Testing", "DevOps", "Embedded", "Security"],
                      ["Gaming", "AI", "Big Data"]]

print(tabulate(cities))
print("Type locations after space:")
input_locations = list(map(str, input().split()))

print(tabulate([["Stażysta", "Junior", "Mid", "Expert"]]))
print("Type job levels after spaces:")
input_level = list(map(str, input().split()))

print(tabulate(categories))
print("Choose categories after spaces:")
input_categories = list(map(str, input().split()))

print("Wait, opening the browser...")

Browser = no_fluff_jobs.BrowserBot()

Browser.choose_location_filters(input_locations)
Browser.click_confirm_button()

Browser.choose_level_filters(input_level)
Browser.click_confirm_button()

Browser.choose_category(input_categories)
Browser.click_confirm_button()

Browser.collect_job_offers()
Browser.close_browser()
Browser.print_job_offers()
