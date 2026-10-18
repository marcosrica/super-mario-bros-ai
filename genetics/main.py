from Entities.Mario import Mario
from classes.Level import Level
from classes.Wrapper import Wrapper
from genetics.Genes import Genes


def main():
    population_count = 100
    enviroments: list[Wrapper] = []
    models: list[Wrapper] = []
        
    test_enviroment:Wrapper = Wrapper("./level1-2", True, 1000)
    test_model = Genes(1000, 0.1)
    
    test_enviroment.set_model(test_model)
    test_enviroment.simulate()
    
    test_mario_res, test_level_res = test_enviroment.get_state()
    test_max = test_enviroment.get_max_mario_pos()

    print("Mario reached an score of ", evaluate(test_mario_res, test_level_res, test_max))


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