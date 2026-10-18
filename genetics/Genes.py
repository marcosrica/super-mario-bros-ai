import random as rd
import numpy as np

from classes.PlayerWrapper import PlayerWrapper


class Genes(PlayerWrapper):
    def __init__(self, genes_count, mutation_range):
        self.mutation_range = mutation_range
        self.counter = 0
        self.genes_count = genes_count
        self.genome = np.zeros(genes_count)
        self.options = [0, 1, 2, 3, 4]

        for i in range(genes_count):
            self.randomize_gene(i)

    def randomize_gene(self, gene_pos):
        self.genome[gene_pos] = rd.choice(self.options)

    def make_move(self):
        self.counter = self.counter + 1
        return self.genome[self.counter - 1]

    def moves_left(self):
        return (self.genes_count - self.counter) != 0
    