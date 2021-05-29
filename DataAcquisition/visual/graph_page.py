from dv import Graph

class GraphPage:

    def __init__(self, page_name = None):
        self.page_name = page_name
        self.graph = Graph()
        self.var_list = self.graph.titles
        self.x = self.var_list[0]
        self.y = [self.var_list[1], self.var_list[2]]
        self.graph.x_axis = self.x
        self.graph.y_axis = self.y


    def create_graph(self, x, y):
        self.x = x
        self.y = y
        self.graph.x_axis = x
        self.graph.y_axis = y

    
