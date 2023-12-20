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
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        # 'Cookie': 'GCs=CartItem1_92_03_87_UserName1_92_4_02_; MISCGCs=USERPC1_92_021083_87_USERLL1_92_42.3581%2C-71.06473_87_USERST1_92_MA3_87_USERDMA1_92_5063_87_DT1_92_PC; SEED=-4620719122405781010%7C1026-21%2C1044-21%7C1028-21%2C1069-21%2C1086-21%2C1114-21%2C1167-21%2C1203-21%2C601-25%2C662-23%2C979-21%2C983-21; SignedIn=0; _abck=3C380C4FA3079BAE860EF38FD9DEA7D5~-1~YAAQp7xuaFJW90WMAQAAT2NAbAuzwybewzssJEJW/tRUKFIm4Bmt/GAmilkqLS+0nsfZB/7DUoi2hC074jU8LjMfg07aB6uldwrpWckbaX721X9ZaIwQjMgwIlvkWfiqJeHV4poFehid4I3ee5nv56xEFWxlD9mkamleiVqgQdlZtcqa/tq35UtP29or2pY32rA6YmlyXgKZAnmby+wxTvQnqJJAuQ8FktyOPVAeF9OZrcz8JwwpPT22ItTgqgX++SS8LljPurSISweRyzIKoXRaGr2N92obQwIfUYlQxQdyqFZVV36u6Way1uI0w2DsMO3Dl7IiTKLQnRW4VJkU9Rl6pcWlkwJSND0jVoKaDbiHolHr0kLiVqdExL7l+8CcWWwAlqPnMA6L~-1~-1~1702083957; bm_sz=C953B453527AF5E3FD46F53E1FFF538F~YAAQp7xuaFNW90WMAQAAT2NAbBZ3ZwEEsDkV1SiodVTdrxth1k20ZSdeGxPdhgq4RNmL69k5drPTFGI5hNzWE+Mz0Ps1oak3ZxCr5k5k0SDDs+QODwUwWsW188EGbnE9Tc1eTiIs6sEzraF9BjFpcNnIrYr7IE/naeqU7E279k6yFEhyudR7Oi8aIIYBvlbYOO47VNRvFTbHDcpPzOM0z9lyzovl/EqHcjLC3hdc1COqOUssKe2Z7MLJGdE+WI03g30M8N1TgUzVS8ktYjkO2ZZOmLHxRJNi5bcovKatN8b+AQ==~4600625~3618374; currency=USD; mercury=true; shippingCountry=US; akavpau_www_www1_macys=1702623544~id=73a829acbeb123313f015d0dc7d1ef2e'
        # "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
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
