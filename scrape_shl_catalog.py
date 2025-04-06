from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# URL to scrape
base_url = "https://www.shl.com/solutions/products/product-catalog/"

# Path to ChromeDriver
chromedriver_path = "F:/Project/SHL/chromedriver.exe"

# Test type mapping from tooltip
test_type_map = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

def get_duration(driver, url):
    driver.get(f"https://www.shl.com{url}")
    time.sleep(3)  # Adjust as needed
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # This is a guess—inspect actual pages to find the correct tag/class
    duration_elem = soup.find("span", class_="duration") or soup.find("p", string=lambda x: "min" in x.lower() if x else False)
    return duration_elem.text.strip() if duration_elem else "N/A"

try:
    if not os.path.exists(chromedriver_path):
        raise FileNotFoundError(f"ChromeDriver not found at {chromedriver_path}")

    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service)

    assessments = []
    page = 0
    max_pages = 32

    while page < max_pages:
        url = f"{base_url}?start={page * 12}&type=1" if page > 0 else base_url
        print(f"Scraping page {page + 1}: {url}")
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        if page == 0:
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Page title:", soup.title.text if soup.title else "No title found")

        items = soup.select("table tbody tr")
        print(f"Found {len(items)} assessment items on page {page + 1}")

        if not items:
            break

        for item in items:
            title_td = item.find("td", class_="custom__table-heading__title")
            name = title_td.find("a").text.strip() if title_td and title_td.find("a") else "Unknown"
            link = title_td.find("a")["href"] if title_td and title_td.find("a") else "#"

            if name == "Unknown":
                continue

            td_elements = item.find_all("td", class_="custom__table-heading__general")
            remote_testing = "Yes" if len(td_elements) > 0 and td_elements[0].find("span", class_="catalogue__circle -yes") else "No"
            adaptive = "Yes" if len(td_elements) > 1 and td_elements[1].find("span", class_="catalogue__circle -yes") else "No"

            keys_td = item.find("td", class_="product-catalogue__keys")
            keys = keys_td.find_all("span", class_="product-catalogue__key") if keys_td else []
            test_type = ", ".join(test_type_map.get(key.text.strip(), "Unknown") for key in keys) if keys else "N/A"

            # Fetch duration from the individual page
            duration = get_duration(driver, link)

            print(f"Name: {name}, Link: {link}, Remote: {remote_testing}, Adaptive: {adaptive}, Type: {test_type}, Duration: {duration}")
            assessments.append({
                "Assessment Name": name,
                "URL": link,
                "Remote Testing Support": remote_testing,
                "Adaptive/IRT Support": adaptive,
                "Duration": duration,
                "Test Type": test_type
            })

        page += 1

    driver.quit()

    df = pd.DataFrame(assessments)
    df.to_csv("shl_assessments.csv", index=False)
    print(f"Data scraped and saved to shl_assessments.csv with {len(assessments)} entries")

except Exception as e:
    print(f"An error occurred: {e}")
    if 'driver' in locals():
        driver.quit()