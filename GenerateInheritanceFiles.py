import sys
sys.path.append("../inspyred/inspyred/")
import ec
import inspyred
from random import Random
from time import time
import ec


if __name__ == '__main__':
    prng = Random()
    prng.seed(time()) 

    problem = inspyred.benchmarks.Rastrigin(2)
    ea = inspyred.ec.GA(prng)
    ea.observer = inspyred.ec.observers.file_observer
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    final_pop = ea.evolve(generator=problem.generator,
                          evaluator=problem.evaluator, 
                          pop_size=150, 
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          max_evaluations=2500,
                          inheritance=True)
    best = max(final_pop)
    print('Best Solution: \n{0}'.format(str(best)))
