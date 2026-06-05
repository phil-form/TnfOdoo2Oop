class MyList(list):
    def __init__(self, value):
        self.value = value

    # Je n'ai plus qu'a surcharger les méthodes dont j'ai besoin.

myList = MyList(55)
