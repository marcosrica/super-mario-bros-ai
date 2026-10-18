from operator import attrgetter

from Entities.Mario import Mario
from classes.Level import Level
from classes.Wrapper import Wrapper
from genetics.Genes import Genes
import numpy as np

def main():
    level_name = "./level1-2"
    draw = True
    frames = 60
    gene_count = 1000
    mutation_chance = 0.1
    
    population_count = 100
    generation_count = 1
    save_every = 5
    
    enviroments, models = make_initial_generation(population_count, level_name, draw, frames, gene_count, mutation_chance)

    try:
        models = load_generation("./genetics/save.npy", models)
        print("Resuming saved generation")
    except Exception:
        print("Could not retrieve any previous generation. Starting from scratch")
        
    while True:
        #Running a generation
        print()
        print(f"--- Running generation number {generation_count} ---")
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
            models[i].set_score(score)
            print(f"Mario nº{i} of generation {generation_count} scored {score}")

            #Cleaning up the enviroment
            enviroments[i].reset_enviroment()

        #Sorting the models based on the results
        models = sorted(models, key=attrgetter("score"), reverse=True)
        print(models)

        #Combining
        print(f"Combining the results of generation {generation_count}")
        models = combine(models)

        if generation_count % save_every:
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
    score += mario.get_pos()[0]

    #Then penalise individuals who have gotten really far, but then returned
    difference = max_pos - score
    score -= (2 * difference)

    #Then for the amounts of points scored
    score += level.points

    #Then for the amount of coins (with a buff)
    score += (100 * level.coins)

    #Last, heavily penalise Mario if dead
    if mario.restart:
        score -= 500

    #Return the composed score
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

def load_generation(route, population: list[Genes]):
    arr = np.load("./genetics/save.npy")
    for i in range(len(arr)):
        for k in range(len(arr[0])):
            population[i].genome[k] = arr[i][k]

    return population