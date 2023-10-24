import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

url = 'https://chandra.harvard.edu/photo/description_audio.html'

response = requests.get(url)
response.raise_for_status()  #  exception if the request was unsuccessful

# parse the HTML content 
soup = BeautifulSoup(response.text, 'html.parser')

img_tags = soup.find_all('img')[2:]  # Skip the first two images (decorative images)
description_links = soup.find_all('a', href=True)

#these will hold the links
images = []
descriptions = []

for img in img_tags:
    src = img.get('src')
    if src:
        images.append(src)

for link in description_links:
    href = link.get('href')
    if href and "description.txt" in href:
        descriptions.append(href)

# need a  base URL
base_url = 'https://chandra.harvard.edu/'

# join the base URL with the extracted path or URL
for index, img_url in enumerate(images):
    images[index] = urljoin(base_url, img_url)

for index, desc_url in enumerate(descriptions):
    descriptions[index] = urljoin(base_url, desc_url)

# make a dir to save downloads
pairs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pairs")
os.makedirs(pairs_dir, exist_ok=True)  # Create directory if it doesn't exist

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):  # 8k chunks
                f.write(chunk)
    return local_filename

for i, (img_url, desc_url) in enumerate(zip(images, descriptions)):
    pair_dir = os.path.join(pairs_dir, f"pair_{i}")
    os.makedirs(pair_dir, exist_ok=True)

    # define local file names
    local_img_name = os.path.join(pair_dir, f"image.{img_url.split('.')[-1]}")
    local_desc_name = os.path.join(pair_dir, "description.txt")

    try:
        # download image
        download_file(img_url, local_img_name)
        print(f"image {i} downloaded: {local_img_name}")

        # download description
        download_file(desc_url, local_desc_name)
        print(f"description {i} downloaded: {local_desc_name}")
    except Exception as e:
        print(f"error indownloading {img_url} or {desc_url}: {e}")
