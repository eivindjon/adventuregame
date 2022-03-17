def read_page(pn:int) -> list:
    from json import loads
    with open("game.json") as file:
        data = file.read()
    lst = loads(data)
    print(lst[pn][0])
    return lst[pn][1]
