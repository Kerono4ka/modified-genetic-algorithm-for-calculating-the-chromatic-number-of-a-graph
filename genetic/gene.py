import operator
from random import randint, choice  # random N, A<=N<=B, randint(A,B)

from graph.graph import Graph
from util.params import Params


def swap(array, i, j):
    """меняет местами два элемента в массиве"""
    arr2 = array[:]
    arr2[i], arr2[j] = arr2[j], arr2[i]
    return arr2


def get_any_wrongly_colored_node(arr, graph):
    """проверяет, окрашены ли вершины на двух концах ребра в одинаковый цвет.
       если да, то возвращает одну из вершин"""
    for edge in graph.edges:
        if arr[edge.start] == arr[edge.end]:   # arr[edge.start] это будет цвет вершины, где начинается ребро
            return edge.start                  # edge.start\edge.end это вершины графа
    return 1


def get_worst_placed_node(arr, graph):
    """находит такую вершину графа, которая имеет наибольшее количество смежных вершин с таким же цветом"""
    scores_dict = {}
    # считает кол-во смежных вершин с таким же цветом
    for edge in graph.edges:
        if arr[edge.start] == arr[edge.end]:
            if edge.start in scores_dict:
                scores_dict[edge.start] += 1
            else:
                scores_dict[edge.start] = 1

            if edge.end in scores_dict:
                scores_dict[edge.end] += 1
            else:
                scores_dict[edge.end] = 1
    try:
        return max(scores_dict.items(), key=operator.itemgetter(1))[0]  # itemgetter(1) сортируем по эл. с
    except ValueError:                                                  # индексом 1 (т.е. по значению)
        return randint(0, len(graph.points) - 1)  # max()[0] это нашли max значение и [0] берем его ключ


def get_final_color(worst_pos, array, graph):   # worst_pos вершина графа смежная с
                                                # max кол-вом вершин того же цвета
    """ записываем в словарь все вершины смежные с worst_pos, проверяем их цвета,
        исходя из этого находим цвет, в который окрашено минимальное количество смежных с worst_post вершин,
        т.е. находим наиболее валидный цвет из УЖЕ имеющихся"""
    connected_nodes = []    # все вершины, связанные с worst_pos, не включая саму worst_pos
    for edge in graph.edges:
        if edge.start == worst_pos:
            connected_nodes.append(edge.end)
        if edge.end == worst_pos:
            connected_nodes.append(edge.start)

    colors_dict = {}  # словарь=  цвет: кол-во вершин этого цвета
    for i in set(array):
        colors_dict.update({i: 0})   # заполняем словарь нулями

    # итерируемся по смежным с worst_pos вершинам
    # узнаем их цвет, и находим этот цвет в словаре colors_dict
    # увеличиваем значение этого цвета на один
    for node in connected_nodes:
        colors_dict[array[node]] += 1

    # получение ключа из той пары в словаре, значение у которой самое большое
    return min(colors_dict.items(), key=operator.itemgetter(1))[0]


class Gene:
    """одна хромосома (один массив) - одна вероятная раскраска графа"""
    def __init__(self, array):
        self.array = array

    def reproduce(self, obj2):    # reproduce = порождать,воспроизводить
        """кроссовер_1
           половину генов берем от self.array, половину от obj2"""
        part_a = []
        part_b = []

        for i in range(Graph.no_points):
            if i < Graph.no_points / 2:
                part_a.append(self.array[i])
            else:
                part_b.append(obj2.array[i])

        progeny = []     # потомство
        for i in range(Graph.no_points):
            if i < Graph.no_points / 2:
                progeny.append(part_a.pop(0))
            else:
                progeny.append(part_b.pop(0))
        return Gene(progeny)

    def reproduce_1(self, obj2):
        """кроссовер_2
           парный индекс массива - ген берем от первого предка,
           непарный индекс(#цвет)  - от второго предка"""
        progeny = []
        for i in range(Graph.no_points):
            if i % 2 == 0:
                progeny.append(self.array[i])
            else:
                progeny.append(obj2.array[i])
        return Gene(progeny)

    def evaluate(self, graph):
        """ фитнесс-функция
            penalty_same_color за каждую смежную вершину того же цвета
            (т.е снятие штрафа, если у ребра на концах вершины одинаковых цветов)
            и penalty_per_color_used за каждый использованный цвет """
        evaluation = 0
        for edge in graph.edges:
            if self.array[edge.start] == self.array[edge.end]:
                evaluation += Params.penalty_same_color
        # снимаем penalty_per_color_used (=1) за каждый использованный цвет
        # для этого преобразуем список в множество:
        # set([0,4,6]) = 3, set([0,4,4]) = 2, set([0,0,0]) = 1
        evaluation += len(set(self.array)) * Params.penalty_per_color_used
        # чем выше счет у хромосомы, тем должно быть лучше. Т.е. идеальный счет пустого графа = 0
        # а дальше за кол-во цветов и за ошибки счет отнимается. Получается, чем он выше(ближе к 0), тем лучше
        return -1 * evaluation

    def mutate(self, graph=None):
        """ меняет местами два рандомных гена """
        i = randint(1, len(self.array) - 1)
        j = randint(1, len(self.array) - 1)
        return Gene(swap(self.array, i, j))

    def mutate_1(self, graph):
        """ присваеваем "худшей" вершине наиболее валидный цвет из УЖЕ имеющихся цветов,
            исходя из цветов смежных ей вершин """
        worst_pos = get_worst_placed_node(self.array, graph)  # искомая худшая вершина
        final_color = get_final_color(worst_pos, self.array, graph)
        new_arr = self.array[:]
        new_arr[worst_pos] = final_color
        return Gene(new_arr)

    def mutate_2(self, graph):
        """ присваеваем "худшей" вершине рандомный цвет из уже имеющихся """
        worst_pos = get_worst_placed_node(self.array, graph)
        new_arr = self.array[:]
        new_arr[worst_pos] = choice(list(set(self.array)))
        return Gene(new_arr)

    def mutate_3(self, graph):
        """ находим первую неправильно раскрашенную вершину и красим ее в валидный цвет
            из УЖЕ имеющихся цветов"""
        pos = get_any_wrongly_colored_node(self.array, graph)
        new_arr = self.array[:]
        new_arr[pos] = get_final_color(pos, self.array, graph)
        return Gene(new_arr)

    def mutate_4(self, graph):
        """ находим первую неправильно раскрашенную вершину и красим ее в РАНДОМНЫЙ цвет
            из УЖЕ имеющихся цветов """
        pos = get_any_wrongly_colored_node(self.array, graph)
        new_arr = self.array[:]
        new_arr[pos] = choice(list(set(self.array)))
        return Gene(new_arr)

    def __str__(self):
        return str(self.array)
