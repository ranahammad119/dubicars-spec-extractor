from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up headless Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Launch ChromeDriver
driver = webdriver.Chrome(options=options)

# Target DubiCars listing URL
url = "https://www.dubicars.com/2025-toyota-land-cruiser-land-cruiser-vxr-33l-black-665972.html"
driver.get(url)
time.sleep(7)

print("Page title:", driver.title)
print("Looking for specs section...")

soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

specs_section = soup.select_one("div.main #item-specifications")
print(specs_section.prettify())  # 👀 Show the raw HTML inside the specs section


# Find the new container with specs
specs = {}
spec_list = soup.select("ul.faq__data > li")

if spec_list:
    print("✅ Found list-based specs!")
    for li in spec_list:
        spans = li.find_all("span")
        if len(spans) == 2:
            key = spans[0].get_text(strip=True)
            value = spans[1].get_text(strip=True)
            specs[key] = value
else:
    print("❌ Spec list not found!")

print("\n✅ Extracted Car Specifications:\n")
for key, value in specs.items():
    print(f"{key}: {value}")
