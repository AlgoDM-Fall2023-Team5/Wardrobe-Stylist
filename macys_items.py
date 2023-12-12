import requests
from bs4 import BeautifulSoup
import time

def fetch_product_info(*keywords):
    print(keywords)
    base_url = "https://www.macys.com/shop/search?keyword=" + "+".join(keywords)

    headers = {
        'authority': 'www.macys.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }

    # Send a request to get the product information
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract product containers
        product_containers = soup.find_all('div', class_='productThumbnail')

        # Create a list to store product information
        products = []

        for container in product_containers:
            # Extract image URL
            img_element = container.find('img', class_='thumbnailImage')
            image_url = img_element['src'] if img_element and 'src' in img_element.attrs else None

            # Extract product URL
            product_url_element = container.find('a', class_='productDescLink')
            product_url = product_url_element['href'] if product_url_element else None

            if image_url and product_url:
                products.append({
                    'image_url': image_url,
                    'product_url': product_url
                })

        time.sleep(2)

        return products

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    keywords = ['a', 'b', 'c', 'd']
    result = fetch_product_info(*keywords)
    print(type(result))
    if result:
        for product in result:
            print(f"Image URL: {product['image_url']}")
            print(f"Product URL: {product['product_url']}")
            print("\n")
