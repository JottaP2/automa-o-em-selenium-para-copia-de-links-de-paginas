from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests

driver = webdriver.Chrome()

driver.get("https://www.cnnbrasil.com.br/")

time.sleep(5)

def find_links(max_links=100):
    visited_links = set()
    
    new_links = driver.find_elements(By.CSS_SELECTOR, "a")

    with open("links.txt", "w") as file:
        for link_element in new_links:
            href = link_element.get_attribute("href")
            if href and href.startswith("http") and href not in visited_links:
                visited_links.add(href)
                
                # Tentar acessar a página
                try:
                    response = requests.get(href, timeout=5)
                    status = response.status_code
                    if status == 200:
                        file.write(f"Acessível: {href}\n")
                        print(f"Link acessível: {href}")
                    else:
                        file.write(f"Inacessível (Status {status}): {href}\n")
                        print(f"Link inacessível (Status {status}): {href}")
                except requests.exceptions.RequestException as e:
                    file.write(f"Inacessível (Erro): {href}\n")
                    print(f"Link inacessível (Erro): {href} - {str(e)}")
                
                if len(visited_links) >= max_links:
                    break  

    print(f"Links encontrados e salvos: {len(visited_links)}")
    driver.quit()

find_links(max_links=100)