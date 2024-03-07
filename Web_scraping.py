from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time
import csv

def initialize_browser():
    print("Inicjalizacja przeglądarki...")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    print("Przeglądarka zainicjalizowana.")
    return driver

    # Pobieranie linków do drzewek technologicznych
def get_tree_links(driver, url):
    print(f"Otwieranie strony głównej drzewek technologicznych: {url}")
    driver.get(url)
    sleep(2) 
    print("Pobieranie linków do drzewek technologicznych...")
    elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/techtree/']")
    links = [element.get_attribute('href') for element in elements]
    print(f"Znaleziono {len(links)} linków do drzewek technologicznych.")
    return links

    # Otwieranie strony drzewka technologicznego
def get_tank_links(driver, tree_url):
    print(f"Otwieranie strony drzewka technologicznego: {tree_url}")
    driver.get(tree_url)
    sleep(2)
    print("Pobieranie linków do czołgów...")
    elements = driver.find_elements(By.CSS_SELECTOR, "a[href*='/tank/']")
    links = [element.get_attribute('href') for element in elements]
    print(f"Znaleziono {len(links)} linków do czołgów.")
    return links
    
    # Otwieranie strony czołgu
def get_tank_stats(driver, tank_url):
    print(f"Otwieranie strony czołgu: {tank_url}")
    driver.get(tank_url)
    sleep(2)
    print("Pobieranie statystyk czołgu...")
    stats_elements = driver.find_elements(By.CSS_SELECTOR, "div.stat-line")
    stats = {}
    for element in stats_elements:
        label = element.find_element(By.TAG_NAME, "label").text
        value = element.find_element(By.TAG_NAME, "span").text
        stats[label] = value
    print("Statystyki czołgu pobrane.")
    return stats

def main():
    start_time = time.time()
    driver = initialize_browser()
    base_url = "https://tanks.gg/techtree/germany"  # startowy URL
    tree_links = get_tree_links(driver, base_url)

    all_tanks_stats = {}
    for tree_link in tree_links:
        tank_links = get_tank_links(driver, tree_link)
        for tank_link in tank_links:
            tank_name = tank_link.split('/')[-1] 
            tank_stats = get_tank_stats(driver, tank_link)
            all_tanks_stats[tank_name] = tank_stats
            

    print("Zapisywanie danych do pliku CSV...")
    csv_file_path = "C:\\studia\\python\\projekt_web_scraping\\tanks_stats.csv"
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        headers = ['Tank Name', 'Statistic', 'Value']
        writer.writerow(headers)
        
        for tank_name, stats in all_tanks_stats.items():
            for stat, value in stats.items():
                writer.writerow([tank_name, stat, value])
    print(f"Dane zostały zapisane do {csv_file_path}")

    print("Zamykanie przeglądarki...")
    driver.quit()
    end_time = time.time()
    print(f"Całkowity czas wykonania programu: {int((end_time - start_time) // 60)} min i {int((end_time - start_time) % 60)} sekund")

if __name__ == "__main__":
    main()

