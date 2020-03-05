class Graph:
# переменные должны быть инкапсулированны через getter\setter
    no_points = 0

    def __init__(self, points, edges):
        Graph.no_points = len(points)
        self.points = points  # а тут присваиваются массивы
        self.edges = edges

    def __str__(self):
        """ [перечень всех вершин]
            [перечень всех ребер] """
        points = '['
        for point in self.points:
            points += str(point)
        points += ']'
        edges = '['
        for edge in self.edges:
            edges += str(edge)
        edges += ']'
        return points + "\n" + edges
