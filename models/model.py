class Model:
    def __init__(self, name):
        self.name = name
        self.model = None
        self.scale = None

    def get_name(self):
        return self.name

    def learning(self, vectors):
        pass

    def detection(self, vector):
        pass
