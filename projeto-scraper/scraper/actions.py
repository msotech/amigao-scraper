import requests
from bs4 import BeautifulSoup

def parse_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    return None

def determine_offer(soup):
    return soup.find(attrs={"data-price-type": "oldPrice"}) is not None

def extract_product_name(soup):
    product_name_element = soup.find(attrs={"itemprop": "name"})
    return product_name_element.text.strip() if product_name_element else None

def extract_product_sku(soup):
    sku_element = soup.find(attrs={"data-product-sku": True})
    return sku_element["data-product-sku"] if sku_element else None

def extract_offer_prices(soup):
    old_price_element = soup.find(
        attrs={"data-price-type": "oldPrice", "data-price-amount": True}
    )
    new_price_element = soup.find(
        attrs={"data-price-type": "finalPrice", "data-price-amount": True}
    )

    old_price = old_price_element["data-price-amount"] if old_price_element else None
    new_price = new_price_element["data-price-amount"] if new_price_element else None

    return old_price, new_price

def extract_normal_price(soup):
    price_element = soup.find(
        attrs={"data-price-type": "finalPrice", "data-price-amount": True}
    )
    return price_element["data-price-amount"] if price_element else None

def extract_product(url):
    soup = parse_url(url)
    if not soup:
        print(f"Failed to fetch data from URL: {url}")
        return None

    offer = determine_offer(soup)

    if offer:
        old_price, current_price = extract_offer_prices(soup)
    else:
        old_price = None
        current_price = extract_normal_price(soup)

    sku = extract_product_sku(soup)
    name = extract_product_name(soup)

    if not name or not sku or not current_price:
        print(f"Failed to extract all product details from URL: {url}")
        return None

    product_data = {
        "name": name,
        "sku": sku,
        "current_price": float(current_price),
        "old_price": float(old_price) if old_price else None,
        "offer": offer,
    }
    return product_data
