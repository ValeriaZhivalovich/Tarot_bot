import requests
from bs4 import BeautifulSoup
import sqlite3
import time

# Создание базы данных SQLite
def create_database():
    conn = sqlite3.connect("tarot_cards.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            name TEXT,
            position TEXT,
            sphere TEXT,
            meaning TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Сохранение данных в базу
def save_to_database(card_name, position, sphere, meaning):
    conn = sqlite3.connect("tarot_cards.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cards (name, position, sphere, meaning) VALUES (?, ?, ?, ?)
    ''', (card_name, position, sphere, meaning))
    conn.commit()
    conn.close()

# Сбор информации с одной страницы карты
def parse_card(card_url, card_name):
    response = requests.get(card_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    positions = ['Прямое', 'Перевернутое']
    spheres = ['Общее', 'Любовь', 'Работа', 'Ситауция', 'Финансы', 'Здоровье','Духовное','Совет Карты','Карта дня']
    
    for position in positions:
        for sphere in spheres:
            sphere_section = soup.find('div', class_='card-meaning', id=f'{sphere}-{position}')
            if sphere_section:
                meaning = sphere_section.text.strip()
                save_to_database(card_name, position, sphere, meaning)

# Основной процесс сбора данных
def scrape_website():
    base_url = "https://astrometa.ru/znachenie-taro/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Поиск ссылок на все карты
    card_links = soup.find_all('a', class_='card-link')
    for link in card_links:
        card_url = link['href']
        card_name = link.text.strip()
        print(f"Собираем данные для карты: {card_name}")
        parse_card(card_url, card_name)
        time.sleep(1)  # Небольшая пауза, чтобы не перегружать сервер

# Выполнение
if __name__ == "__main__":
    create_database()
    scrape_website()
    print("Сбор данных завершён!")
