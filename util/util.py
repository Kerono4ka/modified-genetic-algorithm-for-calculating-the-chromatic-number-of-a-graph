import random

from graph.edge import Edge
from graph.point import Point


def get_random_points(no_points):
    """ Создает список из no_points вершин
        (присваивает им рандомные х,у координаты) """
    points = []
    points_list = []
    i = 0
    while i < no_points:
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        new_point = Point(x, y)
        new_point_list = [x, y]
        # проверка на повторяющиеся вершины, чтобы не было двух с одинаковыми координатами
        f = False
        for point in points:
            if str(point) == str(new_point):
                f = True
        if not f:
            points.append(new_point)
            points_list.append(new_point_list)
            i += 1
    return points, points_list


def get_random_edges(no_points, no_edges):
    """ добавить корректное кол-во ребер графа для данного количества вершин"""
    edges = []
    edges_list = []
    i = 0
    while i < no_edges:
        start = random.randint(0, no_points - 1)
        end = random.randint(0, no_points - 1)
        f = False
        # проверка на отсутствие петель
        if start == end:
            continue
        else:
            new_edge = Edge(start, end)
            new_edge_list = [start, end]
            # проверка на некорректные ребра, чтобы одинаковых ребер и граф был неориентированный
            # пр. ребро (1,0) равно ребру (0,1)
            for edge in edges:
                if (edge.start == new_edge.start and edge.end == new_edge.end)\
                   or (edge.end == new_edge.start and edge.start == new_edge.end):
                    f = True
            if not f:
                edges.append(new_edge)
                edges_list.append(new_edge_list)
                i += 1
    return edges, edges_list
