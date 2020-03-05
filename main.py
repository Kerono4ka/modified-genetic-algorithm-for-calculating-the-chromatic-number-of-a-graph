from random import choice, randint
from time import perf_counter
from time import sleep
import operator
import json

from genetic.gene import Gene
from genetic.population import Population
from graph.graph import Graph
from util.Stats import Stats
from util.params import Params
from util.util import get_random_points, get_random_edges
from graph.point import Point
from graph.edge import Edge


# graph = None


# это функция из population.py ее можно и не дублировать
# в population.py используется для другой внутренней ф-ции, а тут для своей

def get_random_parent(no_points, colors_used):
    sample_numbers = [0]
    for i in range(no_points - 1):
        sample_numbers.append(randint(0, colors_used - 1))
    return Gene(sample_numbers)


def initialize_population(graph, colors_used):
    # n = Params.initial_population_size
    population = []
    for i in range(Params.initial_population_size):
        population.append(get_random_parent(graph.no_points, colors_used))
    return Population(population)


def do_genetic(population, graph, colors_used):
    """ крутится цикл создания потомства, оценки, опять. Пока не будет stop_genetic_after_count
        повторов """
    iterations = 0
    last_n = [float('Inf')] * Params.stop_genetic_after_count  # список из stop_genetic_after_count элементов,
                                                               # заполненный inf-ами
    best_gene = None
    while True:
        iterations += 1
        max_evaluation = population.get_max_evaluation(graph)  # наибольший счет фит.ф-ции
        last_n.pop(0)  # выкидываем из списка первый элемент
        last_n.append(max_evaluation)  # вставляем в конец списка мах счет фит.ф-ции
        flag = False
        # флаг будет false только если все score (а их stop_genetic_after_count) будут одинаковыми
        # и тогда цикл прервется, будет считаться, что ГА добился наилучшего результата
        for i in range(len(last_n)):
            if i != 0 and last_n[i] != last_n[i - 1]:  # если значения двух последних фит.ф-ций одинаковы
                flag = True                            # то заканчиваем цикл
        if not flag:
            break
        print(max_evaluation)
        best_gene = population.best_n(1, graph)[0]  # возвращает одну лучшую хромосому
        # print(best_gene)
        new_population = population_propogation_default(population, graph, colors_used)
        population = Population(new_population)
    Graph.no_colours = len(set(best_gene.array))
    eval = best_gene.evaluate(graph)
    no_colors = len(set(best_gene.array))
    conflicts = -1 * (eval + (no_colors * Params.penalty_per_color_used)) / Params.penalty_same_color

    return iterations, best_gene, conflicts


def population_propogation_default(population, graph, colors_used):
    """создание популяции детишек из популяции родителей"""
    parents_crossover = population.best_n(Params.crossover_parents, graph)
    parents_mutation = population.best_n(Params.mutation_parents, graph)
    new_population = []
    new_population.extend(population.best_n(Params.propogation_count, graph))
    new_population.extend(population.crossover(parents_crossover))
    new_population.extend(population.mutate(parents_mutation, graph))
    new_population.extend(population.random(Params.random_count, graph.no_points, colors_used))
    return new_population


def find_out_chorom_num(graph):
    diction = {}
    for i in range(graph.no_points):
        diction.update({i: 0})
    for edge in graph.edges:
        diction[edge.start] += 1
        diction[edge.end] += 1
    return max(diction.items(), key=operator.itemgetter(1))[1]


def work(points, edges):
    t1 = perf_counter()
    graph = Graph(points, edges)
    chrom_num = find_out_chorom_num(graph)
    min = 1
    save_result = None
    iterations_sum = 0
    while chrom_num > min:
        result = int((chrom_num + min) / 2)
        population = initialize_population(graph, result)
        iterations, best_gene, conflicts = do_genetic(population, graph, result)
        colors_used = len(set(best_gene.array))
        iterations_sum  += iterations
        time = perf_counter() - t1
        Stats(iterations, time, colors_used, best_gene, conflicts, graph)
        if conflicts == 0:
            chrom_num = result
            save_result = result
        else:
            min = result + 1
    time = perf_counter() - t1
    print("result: ")
    print("colors: ", save_result, " time ", time, "iterations ", iterations_sum)


def in_file():
    no_points = 178
    no_edges = 1484
    if no_edges > no_points * (no_points - 1) / 2:
        raise ValueError('There are too many edges {}'.format(no_edges))
    points, points_list = get_random_points(no_points)
    edges, edges_list = get_random_edges(no_points, no_edges)
    with open('points', 'w') as f:
        json.dump(points_list, f)
    with open('edges', 'w') as f:
        json.dump(edges_list, f)


def out_file():
    with open('points', 'r') as f:
        points_list = json.load(f)
    with open('edges', 'r') as f:
        edges_list = json.load(f)
    points = []
    for point in points_list:
        x = point[0]
        y = point[1]
        new_point = Point(x, y)
        points.append(new_point)
    edges = []
    for edge in edges_list:
        start = edge[0]
        end = edge[1]
        new_edge = Edge(start, end)
        edges.append(new_edge)
    work(points, edges)


#in_file()
out_file()