import main
import random
import sources

if __name__ == '__main__':
    # x = main.main(source="Kinopoisk", desc="Скотт Пилигрим")
    # for elem in x['films']:
    #     try:
    #         if elem["nameRu"] and elem["description"]:
    #             print("Film: " + elem["nameRu"])
    #             print("Description: " + elem["description"] + "\n")
    #     except:
    #         if elem["nameRu"]:
    #             print("Film: " + elem["nameRu"])
    #             print("There is no description" + "\n")

    # # Google test
    # y = main.main(source="Google", desc="Фильм про девушку, которая меняет цвет волос")
    # for elem in y['results'][0:5]:
    #     try:
    #         if elem["title"] and elem["link"] and elem["description"]:
    #             print("Page: " + elem["title"])
    #             print("Description: " + elem["description"])
    #             print("Link: " + elem["link"] + "\n")
    #     except:
    #         if elem["link"]:
    #             print("Link: " + elem["link"] + "\n")

    # Imdb test
    # z = main.main(source="Imdb", desc="Blue haired girl")
    # for elem in z['results']:
    #     try:
    #         if elem["title"] and elem["description"] and elem["image"]:
    #             print("Film: " + elem["title"])
    #             print("Poster: " + elem["image"])
    #             print("Description: " + elem["description"] + "\n")
    #     except:
    #         if elem["title"]:
    #             print("Film: " + elem["nameRu"])
    #             print("There is no description" + "\n")


    # Omdb test
    z = main.main(source="Omdb", desc="horror")
    random.shuffle(z)
    for elem in z[0:3]:
        elem = elem.split("/")[2]
        elem_info = sources.get_info_from_omdb(elem)
        try:
            if elem_info["title"] and elem_info["image"]["url"]:
                print("Film: " + elem_info["title"])
                print("Poster: " + elem_info["image"]["url"] + "\n")
        except:
            if elem_info["title"]:
                print("Film: " + elem_info["title"])
                print("There is no poster" + "\n")

