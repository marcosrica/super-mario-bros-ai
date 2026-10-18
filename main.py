from genetics.main import main as main_genetics
import sys

def main():
    #try:
        argument = sys.argv[1]
        match argument:
            case "help":
                print_help()

            case "--help":
                print_help()

            case "-help":
                print_help()

            case "genetic":
                main_genetics()
                
    #except IndexError:
    #    print("Error running the code. Expected one argument. Printing help...")
    #    print()
    #    print_help()

def print_help():
    print()
    print("--- Super Mario Bros AI ---")
    print("A stripped-down rebuild of the original Super Mario Bros game, taylor-made to train AI algorithms with it")
    print()
    print("Possible parameters allowed:")
    print("> genetic: include this parameter to run the simulation using the genetic algorithm included")
    print("> help: prints this text again, with all the information on how to run the program")

main()