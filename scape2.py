from bs4 import BeautifulSoup
import requests
import os

base_url = 'https://chandra.harvard.edu'

# Function to extract fast facts from a detail page
def get_fast_facts(detail_url):
    response = requests.get(detail_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the fast facts table and extract text
    facts_table = soup.find('table', class_='ff_text')
    fast_facts = ''

    if facts_table:
        rows = facts_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 2:
                fact_label = cols[0].get_text(strip=True)
                fact_value = cols[1].get_text(strip=True)
                fast_facts += f'{fact_label}: {fact_value}\n'

    return fast_facts

# Function to process the main page and find detail page URLs
def process_main_page(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'Photo Album' links on the main page
    album_links = soup.find_all('a', text='[Photo Album]', href=True)

    for link in album_links:
        album_url = base_url + link['href']
        fast_facts = get_fast_facts(album_url)

        if fast_facts:
            # Extract a name for the file from the album URL
            file_name = album_url.split('/')[-2] + '.txt'
            file_path = os.path.join('fast_facts', file_name)

            if not os.path.exists('fast_facts'):
                os.makedirs('fast_facts')

            with open(file_path, 'w') as file:
                file.write(fast_facts)
                print(f'Saved fast facts in {file_path}')

# Main execution
main_page_url = base_url + '/photo/description_audio.html'
process_main_page(main_page_url)
