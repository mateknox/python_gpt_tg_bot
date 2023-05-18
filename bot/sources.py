import requests
import json
import config


def get_info_from_kp(desc):
    get_string = "https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword?keyword=" + desc
    # insert your api-key
    headers = {"accept": "application/json", "X-API-KEY": config.KP_TOKEN}
    r = requests.get(url=get_string, headers=headers)
    json_films = json.loads(r.text)
    return json_films


def get_info_from_google(desc):
    # insert your api-key
    get_string = "https://google-search3.p.rapidapi.com/api/v1/search/q=" + desc
    headers = {
        "X-User-Agent": "desktop",
        "X-Proxy-Location": "EU",
        "X-RapidAPI-Key": config.GOOGLE_TOKEN,
        "X-RapidAPI-Host": "google-search3.p.rapidapi.com"
    }
    r = requests.get(url=get_string, headers=headers)
    google_response = json.loads(r.text)
    return google_response


def get_info_from_imdb(desc):
    # insert your api-key to url
    get_string = f"https://imdb-api.com/en/API/Search/{config.IMDB_TOKEN}/" + desc
    headers = {"accept": "application/json"}
    r = requests.get(url=get_string, headers=headers)
    json_films = json.loads(r.text)
    return json_films


def get_titles_from_omdb(desc):
    # insert your api-key to url
    get_string = "https://online-movie-database.p.rapidapi.com/title/v2/get-popular-movies-by-genre"
    headers = {
        "X-RapidAPI-Key": config.OMDB_TOKEN,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }
    query = {"genre": desc, "limit": "100"}
    r = requests.get(url=get_string, headers=headers, params=query)
    json_films = json.loads(r.text)
    return json_films


def get_info_from_omdb(title):
    # insert your api-key to url
    get_string = "https://online-movie-database.p.rapidapi.com/title/get-details"
    headers = {
        "X-RapidAPI-Key": config.OMDB_TOKEN,
        "X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
    }
    query = {"tconst": title}
    r = requests.get(url=get_string, headers=headers, params=query)
    json_films = json.loads(r.text)
    return json_films
