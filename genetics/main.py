from operator import attrgetter
from statistics import mode

from Entities.Mario import Mario
from classes.Level import Level
from classes.Wrapper import Wrapper
from genetics.Genes import Genes
import numpy as np

def main():
    print()
    print("--- Entering genetic evolution mode ---")
    print("Do you want to just train, or do you want to see the game?")
    j_train = ""
    while not (j_train == "Y" or j_train=="y" or j_train == "N" or j_train=="n"):
        j_train = input("> Just train? (Y/n): ")

    if j_train == "Y" or j_train == "y":
        train(False, 10000)
    else:
        train(True, 120)

def train(to_draw:bool, max_frames:int):
    level_name = "./level1-2"
    draw = to_draw
    frames = max_frames
    gene_count = 50
    gene_increment = 50
    mutation_chance = 0.1
    
    population_count = 100
    generation_count = 1
    save_every = 5

    try:
        print("Trying to load a previous session...")
        models, enviroments, gene_count = load_generation(level_name, draw, frames, "./genetics/save.npy", mutation_chance, gene_increment)
        print("Resuming saved generation")
    except Exception:
        print("Could not retrieve any previous generation. Starting from scratch")
        enviroments, models = make_initial_generation(population_count, level_name, draw, frames, gene_count, mutation_chance)

    last_best = 0
        
    while True:
        #Running a generation
        print()
        print(f"--- Running generation number {generation_count} ---")
        total = 0
        
        for i in range(population_count):
            #First set the model
            enviroments[i].set_model(models[i])

            #Simulate the enviroment
            enviroments[i].simulate()

            #getting the results
            mario_res, level_res = enviroments[i].get_state()
            max_res = enviroments[i].get_max_mario_pos()

            #Calculating and saving the score
            score = evaluate(mario_res, level_res, max_res)
            total = total + score
            models[i].set_score(score)

            #Cleaning up the enviroment
            enviroments[i].reset_enviroment()

        #Sorting the models based on the results
        models = sorted(models, key=attrgetter("score"), reverse=True)

        #printing statitics about the generation
        print(f"Total amount of genes for generation: {models[0].genes_count}; mutating from gene {models[0].start_mutations}")
        print(f"Average score of the generation: {total / population_count}")
        print(f"Maximun score of the generation: {models[0].score}")
        print(f"Minimun score of the generation: {models[len(models)-1].score}")

        #Checking if genes should be expanded
        pond_max = models[0].score
        pond_min = models[3 * (population_count // 4)].score
        print(f"pondered values for diversity: {pond_max}; {pond_min}")

        if pond_max != 0 and not enviroments[0].mario.restart:
            difference = pond_min / pond_max
            print(f"Generation similarity: {difference * 100}%")
            if difference > 0.95:
                #Genomes have gotten stuck. Expanding
                print("Generation is stuck. Expanding genome")
                expand_generation(models, gene_increment)
                last_best = models[0].score


        #Combining
        models = combine(models)

        #Checking if we need to save
        if generation_count % save_every == 0:
           save_generation("./genetics/save.npy", models)             

        generation_count = generation_count + 1


def make_initial_generation(population, level_name, draw, frames, gene_count, mutation_chance):
    enviroments: list[Wrapper] = []
    models: list[Genes] = []

    for i in range(population):
        print(f"Making {i}/{population} marios")
        enviroments.append(Wrapper(level_name, draw, frames))
        models.append(Genes(gene_count, mutation_chance))

    return (enviroments, models)

def evaluate(mario:Mario, level:Level, max_pos:int):
    score = 0
    #Rewarding first for how far it went
    score += mario.get_world_x_position() ** 2

    #Then penalise individuals who have gotten really far, but then returned
    difference = max_pos - mario.get_world_x_position()
    score -= (2 * difference)

    #Then for the amounts of points scored
    score += level.points

    #Then for the amount of coins (with a buff)
    score += (100 * level.coins)

    #Last, heavily penalise Mario if dead
    if mario.restart:
        score -= 500

    #Return the composed score, with a slowed down grap
    return score

def combine(models:list[Genes]):
    #Removing the worst half of the last generation
    count = len(models)
    for j in range(int(count/2)):
        models[j].reset()
    
    for j in range(int(count/2), count):
        models[j].set_genes(models[j-int(count/2)].get_genes())
        models[j].reset()

    return models

def save_generation(route, population: list[Genes]):
    arr = np.stack([m.get_genes() for m in population])
    np.save(route, arr)

def load_generation(level_name, draw, frames, route, mut_range, start_mut):
    arr = np.load(route)
    pop_count = len(arr)
    gene_count = len(arr[0])
    population: list[Genes] = []
    enviroments: list[Wrapper] = []
    
    for i in range(pop_count):
        population.append(Genes(gene_count, mut_range))
        population[i].start_mutations = gene_count - start_mut
        population[i].genome = arr[i]

        enviroments.append(Wrapper(level_name, draw, frames))

    return (population, enviroments, gene_count)

def expand_generation(population: list[Genes], expansion):
    for i in range(len(population)):
        population[i].expand_genome(expansion)