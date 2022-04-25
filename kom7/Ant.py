

class Ant:

    # def __init__(self):
    #     self.current_vertex = None
    #     self.tabu_list = []

    def __init__(self, current_vertex=None):
        self.tabu_list = [current_vertex]
        self.current_vertex = current_vertex

    def change_city(self, city):
        self.tabu_list.append(city)
        self.current_vertex = city

