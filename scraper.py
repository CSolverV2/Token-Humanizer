import os
import requests
from bs4 import BeautifulSoup

if not os.path.exists('img'):
    os.makedirs('img')

def download(url, folder_name, image_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(os.path.join(folder_name, image_name), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {image_name}")
        else:
            print(f"Failed to download {image_name}")
    except Exception as e:
        print(f"Exception occurred while downloading {image_name}: {e}")

def scrapit(query, folder_name='img'):
    search_url = f"https://www.google.com/search?q={query}&source=lnms&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    image_tags = soup.find_all('img')
    img_urls = [img['src'] for img in image_tags if 'src' in img.attrs]

    for i, url in enumerate(img_urls):
        download(url, folder_name, f'{query}_{i+1}.jpg')

while True:
    search_query = input("Picture: ")
    scrapit(search_query)
    continue