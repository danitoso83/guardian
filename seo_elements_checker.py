import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import os

URL_FILE = "urls_to_check.txt"
LOG_FILE = "seo_check_log.csv"

def read_urls_from_file():
    with open(URL_FILE, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def check_seo_elements(url):
    try:
        response = requests.get(url, allow_redirects=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        status_code = response.status_code
        
        canonical = soup.find('link', rel='canonical')
        canonical = canonical['href'] if canonical else "N/A"
        
        robots_tag = soup.find('meta', attrs={'name': 'robots'})
        robots_tag = robots_tag['content'] if robots_tag else "N/A"
        
        title = soup.title.string if soup.title else "N/A"
        
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description['content'] if meta_description else "N/A"
        
        h1 = soup.h1.string if soup.h1 else "N/A"

        return [url, status_code, canonical, robots_tag, title, meta_description, h1]
    except Exception as e:
        return [url, str(e), "Error", "Error", "Error", "Error", "Error"]

def main():
    urls = read_urls_from_file()
    
    # Crea o sovrascrive il file di log
    with open(LOG_FILE, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Status Code", "Canonical", "Robots Tag", "Title", "Meta Description", "H1"])
        
        for url in urls:
            print(f"Controllo {url}...")
            result = check_seo_elements(url)
            writer.writerow(result)

    print(f"Controllo completato. I risultati sono stati salvati in {LOG_FILE}")

if __name__ == "__main__":
    main()
