import main

if __name__ == '__main__':
    # x = main.main(source="Kinopoisk", desc="Скотт Пилигрим")
    # for elem in x['films']:
    #     try:
    #         if elem["nameRu"] and elem["description"]:
    #             print("Фильм: " + elem["nameRu"])
    #             print("Описание: " + elem["description"] + "\n")
    #     except:
    #         if elem["nameRu"]:
    #             print("Фильм: " + elem["nameRu"])
    #             print("Описание отсутствует" + "\n")

    # Google test
    y = main.main(source="Google", desc="Фильм про девушку, которая меняет цвет волос")
    for elem in y['results'][0:5]:
        try:
            if elem["title"] and elem["link"] and elem["description"]:
                print("Название страницы: " + elem["title"])
                print("Описание: " + elem["description"])
                print("Ссылка: " + elem["link"] + "\n")
        except:
            if elem["link"]:
                print("Ссылка: " + elem["link"] + "\n")

    # Imdb test
    # z = main.main(source="Imdb", desc="Blue haired girl")
    # for elem in z['results']:
    #     try:
    #         if elem["title"] and elem["description"] and elem["image"]:
    #             print("Фильм: " + elem["title"])
    #             print("Постер: " + elem["image"])
    #             print("Описание: " + elem["description"] + "\n")
    #     except:
    #         if elem["title"]:
    #             print("Фильм: " + elem["nameRu"])
    #             print("Описание отсутствует" + "\n")


