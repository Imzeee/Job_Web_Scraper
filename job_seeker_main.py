import no_fluff_jobs

print("Choose locations by typing names of the cities seperated by spaces")
print("""Avialable options: Warszawa, Wrocław, Kraków, Gdańsk, Poznań, Trójmiasto, Sląśk, Łódź, Katowice 
                Lublin, Szczecin, "Bydgoszcz, Białystko, Gdynia, Gliwice , Sopot""")

input_lokalizacje = list(map(str, input().split()))

print("Choose seniority by typing levels seperated by space")
print("Avialable options: Stażysta, Junior, Mid, Senior, Expert")
input_seniority = list(map(str, input().split()))

print("Wait, collecting data...")

Browser = no_fluff_jobs.BrowserBot()

Browser.find_location_filter("Lokalizacje", input_lokalizacje)

Browser.click_confirm_button()

Browser.find_more_button_filter("Więcej", input_seniority)

Browser.click_confirm_button()

Browser.collect_jobs_descriptions()

Browser.collect_jobs_links()

Browser.scroll_all_pages()

Browser.close_browser()

Browser.print_job_offers()



