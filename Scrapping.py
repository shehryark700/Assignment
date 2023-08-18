import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import json

def scrape_product_info(driver, product_url):
    driver.get(product_url)

    try:
        # Wait until the product name element is present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//h2[@data-qa="product-title"]')))

        # Find the product name
        product_name_element = driver.find_element(By.XPATH, '//h2[@data-qa="product-title"]')
        product_name = product_name_element.text

        # Find the product categories
        product_categories_element = driver.find_element(By.XPATH, '//h1[@class="headline-5=small"]')
        product_categories = product_categories_element.text

        # Find the product image URLs
        product_image_urls = [
            product_image.get_attribute("src")
            for product_image in driver.find_elements(By.CSS_SELECTOR, "div.product-image img")
        ]

        # Find the product description
        product_description_element = driver.find_element(By.XPATH, '//div[@class="description-text text-color-grey mb9-sm ta-sm-c"]/p')
        product_description = product_description_element.text

        # Find the product price
        product_price_element = driver.find_element(By.XPATH, '//div[@data-qa="price"]')
        product_price = product_price_element.text

        # Find the list of available sizes
        product_sizes_element = driver.find_element(By.XPATH, '//span[@class="product-sizes"]')
        product_sizes = product_sizes_element.text.split(", ")

        return {
            "product_name": product_name,
            "product_categories": product_categories,
            "product_image_urls": product_image_urls,
            "product_description": product_description,
            "product_price": product_price,
            "product_sizes": product_sizes
        }
    except Exception as e:
        print(f"Error scraping product: {str(e)}")
        return None

def scrape_product_urls():
    driver = selenium.webdriver.Chrome()
    driver.get("https://www.snkrs.com/en/")
    driver.implicitly_wait(20)

    product_listings = driver.find_elements(By.CLASS_NAME, "product-card")
    product_urls = [product_listing.find_element(By.CSS_SELECTOR, "a").get_attribute("href") for product_listing in product_listings]

    driver.quit()
    return product_urls

if __name__ == "__main__":
    product_urls = scrape_product_urls()

    product_info = []
    driver = selenium.webdriver.Chrome()
    for product_url in product_urls:
        product_data = scrape_product_info(driver, product_url)
        if product_data:
            product_info.append(product_data)

    with open("product_info.json", "w") as json_file:
        json.dump(product_info, json_file, indent=4)

    driver.quit()
    print("Product information saved to product_info.json")