import base64
from secrets_config import spotify_secret_key, spotify_client
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import os
import time


os.environ['SPOTIFY_CLIENT_ID'] = spotify_client
os.environ['SPOTIFY_SECRET_KET'] = spotify_secret_key

client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_SECRET_KET']

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': "Basic " + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {"grant_type": "client_credentials"}
    result = requests.post(url, headers=headers, data=data)
    print(result.text)
    json_result = json.loads(result.content)
    token = json_result['access_token']

    return token


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def search_for_artist(token, artist):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)

    query = f"q={artist}&type=artist&limit=1"
    query_url = f"{url}?{query}"

    result = requests.get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items'][0]

    artist_id = json_result['id']
    return artist_id


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=AR"
    headers = get_auth_header(token)

    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)['tracks']

    return json_result

def get_song_audio_features(token, song_id):
    url = f"https://api.spotify.com/v1/audio-features/{song_id}"
    headers = get_auth_header(token)

    result = requests.get(url, headers=headers)
    json_result = json.loads(result.content)
    keys = ["duration_ms", "energy", "instrumentalness", "speechiness", "valence"]
    filtered_json = { k: json_result[k] for k in keys if k in json_result }

    return filtered_json

def scrape_song(song_name, driver):
    

    search_bar_element = driver.find_element(By.XPATH, '/html/body/div[1]/header/div/div[2]/form/label/input')
    search_bar_element.clear()
    search_bar_element.send_keys(song_name)

    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/header/div/div[2]/div/ul/li[2]/a')))
        first_match_song = driver.find_element(By.XPATH, '/html/body/div[1]/header/div/div[2]/div/ul/li[2]/a')
        first_match_song.click()
        print('...Song found...')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        lyrics_div = soup.find('div', class_='lyric-original')
        lyrics = []
        print('...Lyrics found...')
        for p in lyrics_div.find_all('p'):
            print('...Extracting lyrics...')
            texto = p.get_text(separator="\n").strip()
            if texto:  # Evitás p vacíos
                lyrics.append(texto)

        # Unir todo en un solo string con saltos de línea
        print('...Joining found...')
        full_lyric = "\n\n".join(lyrics)

        return full_lyric

    except:
        print(f"Error scraping song > {song_name}")
        return None

    

    

    


if __name__ == '__main__':
    token = get_token()
    artist = search_for_artist(token, 'drexler')
    songs = get_songs_by_artist(token, artist)
    clean_songs = [{
                'name': song['name'],
                'id': song['id']
            } for song in songs]
    
    print(f'...Found {len(clean_songs)} songs...\n\n')

    driver = webdriver.Chrome()
    driver.get('https://www.letras.com/')
    driver.maximize_window()

    valid_songs = []
    for song_index, song in enumerate(clean_songs):
        print(f'... PROCESSING SONG <<{song["name"]}>>...')
        print('...(1) Enriching with audio features...')
        audio_features = get_song_audio_features(token, song['id'])
        #print(audio_features)
        #print(song)
        song.update(audio_features)
        #print(song)


        print(f'...(2) Scrapping lyrics...')
        song_lyric = scrape_song(song['name'], driver)
        if song_lyric:
            song['lyric'] = song_lyric
            valid_songs.append(song)

        print(valid_songs)


        print('...(3) Sleeping 5 seg before next artist...')

        #break

        time.sleep(5)

    del songs
    del clean_songs

    with open('data/raw_songs.json', 'w', encoding='utf-8') as f:
        json.dump(valid_songs, f, ensure_ascii=False, indent=2)

    
