class Stats(object):
    def __init__(self, iterations, time, colors_used, best_gene, conflicts, graph):
        self.iterations = iterations
        self.time = time
        self.colors_used = colors_used
        self.best_gene = best_gene
        self.conflicts = conflicts
        self.graph = graph

        print('\n     STATS')
        print('iterations : ', iterations)
        print('time : ', time)
        print('colors_used : ', colors_used)
        print('best gene : ', best_gene)
        print('conflicts : ', conflicts)

    def __str__(self):
        return str(len(self.best_gene.array)) + ", " + str(self.iterations) + ", " + str(self.time) + ", " \
               + str(self.colors_used) + ", " + str(self.conflicts) + ", " + str(self.best_gene.evaluate(self.graph))
