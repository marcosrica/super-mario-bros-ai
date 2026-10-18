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
        self.score = 0
        self.start_mutations:int = 0

        for i in range(genes_count):
            self.randomize_gene(i)

    def reset(self):
        self.counter = 0
        self.score = 0

    def __repr__(self):
        return f"Mario(score: {self.score})"

    def get_genes(self):
        return self.genome

    def set_genes(self, new_genes):
        for i in range(self.genes_count):
            if (i > self.start_mutations) and (rd.random() < self.mutation_range):
                self.randomize_gene(i)
            else:
                self.genome[i] = new_genes[i]

    def set_score(self, new_score):
        self.score = new_score

    def randomize_gene(self, gene_pos):
        self.genome[gene_pos] = rd.choice(self.options)

    def make_move(self):
        self.counter = self.counter + 1
        return self.genome[self.counter - 1]

    def moves_left(self):
        return (self.genes_count - self.counter) != 0

    def expand_genome(self, extra_slots:int):
        self.genome = np.concatenate([self.genome, np.zeros(extra_slots, dtype=self.genome[0].dtype)])
        self.start_mutations = self.genes_count

        for i in range(self.genes_count, self.genes_count + extra_slots):
            self.randomize_gene(i)

        self.genes_count += extra_slots