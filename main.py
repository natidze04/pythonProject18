import csv
import time
import requests
from bs4 import BeautifulSoup




def scrape_metacritic_games(pages):
    base_url = 'https://www.metacritic.com/browse/games/release-date/available'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    game_data = []

    for page in range(pages):
        url = f'{base_url}?page={page}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        game_containers = soup.find_all('td', class_='clamp-summary-wrap')

        for container in game_containers:
            title = container.find('h3').text.strip()
            device = container.find('span', class_='data').text.strip()

            genre_element = container.find('span', class_='genre')
            genre = genre_element.text.strip() if genre_element else "N/A"

            game_data.append({'სათაური': title, 'მოწყობილობა': device, 'ჟანრი': genre})

        time.sleep(15)

    return game_data
import csv

def save_to_csv(data, filename):
    keys = data[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


num_pages = 5
game_data = scrape_metacritic_games(num_pages)


save_to_csv(game_data, 'games_data.csv')


for game in game_data:
    print(f"სათაური: {game['სათაური']}, მოწყობილობა: {game['მოწყობილობა']}, ჟანრი: {game['ჟანრი']}")

