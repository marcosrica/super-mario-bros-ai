from operator import attrgetter

from Entities.Mario import Mario
from classes.Level import Level
from classes.Wrapper import Wrapper
from genetics.Genes import Genes


def main():
    level_name = "./level1-2"
    draw = False
    frames = 1000
    gene_count = 1000
    mutation_chance = 0.1
    
    population_count = 4
    generation_count = 1
    
    enviroments, models = make_initial_generation(population_count, level_name, draw, frames, gene_count, mutation_chance)
    print(f"There are {len(enviroments)} marios")

    while generation_count == 1:
        #Running a generation
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

    #Then for the maximun length it has ever reached (with a penalisation)
    score += (max_pos / 4)

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
    pass
    