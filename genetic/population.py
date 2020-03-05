from random import randint

from genetic.gene import Gene
from util.params import Params


class Population:
    def __init__(self, genes, mutation_count=1000, crossover_count=1000, random_count=100):
        self.genes = genes
        self.mutation_count = mutation_count
        self.crossover_count = crossover_count
        self.random_count = random_count

    def best_n(self, n, graph):
        """ возвращает список из n хромосом с самыми высокими счетами фит.ф-ции """
        gene_scores = {}   # словарь=  хромосома: ее счет фитнесс-функции
        for gene in self.genes:
            gene_scores.update({gene: gene.evaluate(graph)})
        # сортировка хромосом (gene_scores) по значению. Хромосомы с самым маленьким счетом фит. фции вначале
        sorted_genes = sorted(gene_scores, key=gene_scores.get)  # dict.get возращает значение по ключу
                                                                 # .get(key) для какого-то определенного ключа
        # sorted_genes это список состоящий из хромосом
        # best_n - кортеж из n хромосом, с лучшими счетами фит.ф-ции
        best_n = sorted_genes[-1 * n:]    # [-1 * n:] выбирает n элементов с хвоста списка
        # self.get_max_evaluation(graph) получаем счет фитнесс ф-ции наилучшей хромосомы в популяции
        # Population(best_n).get_max_evaluation(graph) передаем в конструктор класса кортеж из n лучших генов
        # и для них вызываем ф-цию get_max_evaluation
        if self.get_max_evaluation(graph) > Population(best_n).get_max_evaluation(graph):
            print('ERROR')
        return best_n

    @staticmethod
    def crossover(parents):
        """ функция выбора кроссовера из наявных в gene.py class Gene """
        children = []
        for papa in parents:
            for mummy in parents:
                if not mummy == papa:
                    if Params.crossover_function == "Standard":
                        children.append(mummy.reproduce(papa))
                    elif Params.crossover_function == "Jumbled":
                        children.append(mummy.reproduce_1(papa))
                    elif Params.crossover_function == "None":
                        return []
                    else:
                        print("unknown method : " + Params.crossover_function)
        return children

    @staticmethod
    def mutate(parents, graph):
        """ функция выбора мутации из наявных в gene.py class Gene """
        mutation_function = Params.mutation_function
        children = []
        for parent in parents:
            if mutation_function == "0":
                children.append(parent.mutate())
            elif mutation_function == "1":
                children.append(parent.mutate_1(graph))
            elif mutation_function == "2":
                children.append(parent.mutate_2(graph))
            elif mutation_function == "3":
                children.append(parent.mutate_3(graph))
            elif mutation_function == "4":
                children.append(parent.mutate_4(graph))
            elif mutation_function == "None":
                return []
            else:
                print("unknown method : " + mutation_function)
        return children

    def random(self, random_count, no_points, colors_used):
        """ создание начальной популяции. Возвращает список из хромосом (которые тоже списки)
            получается начальная популяция = random_count"""
        children = []
        for i in range(random_count):
            children.append(self.get_random_parent(no_points, colors_used))
        return children

    def get_random_parent(self, no_points, colors_used):
        """ Создание начальной хромосомы, присваивание всем вершинам рандомных цветов
            при этом количество цветов = кол-во вершин
            передавание готовой хромосомы в конструктор класса Gene """
        sample_numbers = [0]
        for i in range(no_points - 1):
            sample_numbers.append(randint(0, colors_used - 1))
        return Gene(sample_numbers)

    def get_max_evaluation(self, graph):
        """ возвращает счет фитнесс ф-ции наилучшей хромосомы в популяции"""
        max_evaluation = -1 * float("Inf")  # max_evaluation = бесконечность
        for gene in self.genes:
            if gene is None:
                self.genes.remove(gene)
            elif gene.evaluate(graph) > max_evaluation:
                max_evaluation = gene.evaluate(graph)
        return max_evaluation
