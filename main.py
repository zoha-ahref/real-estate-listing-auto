from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time

zillow_link = "https://www.zillow.com"
URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.61529005957031%2C%22east%22%3A-122.25136794042969%2C%22south%22%3A37.5946110002378%2C%22north%22%3A37.95553141811004%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
#https://docs.google.com/forms/d/e/1FAIpQLSeehZozsSb0HD8HcklLex0sxs5dKboc5ohbOXJT1dRUC09k5Q/viewform?usp=sf_link
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
}

response = requests.get(url=URL, headers=headers)
listings_response = response.text

soup = BeautifulSoup(listings_response, "html.parser")
listing = soup.select(".list-card-top a")  #find_all(name=a, .list-card-link)

listing_links = []
for l in listing:
    link = l["href"]
    if "http" not in link:
        listing_links.append(f"https://www.zillow.com{link}")
    else:
        listing_links.append(link)
#print(listing_links)




all_address_elements = soup.select(".list-card-info address")
all_addresses = [address.get_text().split(" | ")[-1] for address in all_address_elements]
print(all_addresses)

listing_price_elements = soup.select(".list-card-heading")      #find_all(name='div', class_='list-card-price')
all_listing_prices = []

for elements in listing_price_elements:
    try:
        # Price with only one listing
        price = elements.select(".list-card-price")[0].contents[0]
    except IndexError:
        print('Multiple listings for the card')
        # Price with multiple listings
        price = elements.select(".list-card-details li")[0].contents[0]
    finally:
        all_listing_prices.append(price)

    #all_listing_prices.append(price.get_text().split("+")[0])
#print(all_listing_prices)

driver_path = "/Users/zohakaukab/Downloads/Development/chromedriver"
driver = webdriver.Chrome(executable_path=driver_path)
for n in range(len(listing_links)):
    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSeehZozsSb0HD8HcklLex0sxs5dKboc5ohbOXJT1dRUC09k5Q/viewform?usp=sf_link")
    time.sleep(2)
    address_text = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')

    price_text = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_text = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    address_text.send_keys(all_addresses[n])
    price_text.send_keys(all_listing_prices[n])
    link_text.send_keys(listing_links[n])
    submit_button.click()

#driver.quit()