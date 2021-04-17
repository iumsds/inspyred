import sys
sys.path.append("../inspyred/inspyred/")
import ec
import inspyred
from random import Random
import time
import math
import os
import tanager

if __name__ == '__main__':
    prng = Random()
    prng.seed(time.time())

    project_name = None

    problem_choice = 0
    while problem_choice not in ['1','2','3','4','5','6','7','8','9']:
        problem_choice = input("~~ Choose Benchmark Problem ~~\n1. Rastrigin\t2. Binary\t\t3. Ackley\n4. Rosenbrock\t5. Schwefel\t\t6. Sphere\n7. Kursawe\t8. Travelling Salesman\t9. Knapsack\nENTER: ")
        if problem_choice not in ['1','2','3','4','5','6','7','8','9']:
            print("Enter the integer corresponding to the your chosen problem")
    if problem_choice == '1':
        problem = inspyred.benchmarks.Rastrigin(2)
        project_name = 'Rastrigin'
    elif problem_choice == '2':
        problem = inspyred.benchmarks.Binary(2)
        project_name = 'Binary'
    elif problem_choice == '3':
        problem = inspyred.benchmarks.Ackley(2)
        project_name = 'Ackley'
    elif problem_choice == '4':
        problem = inspyred.benchmarks.Rosenbrock(2)
        project_name = 'Rosenbrock'
    elif problem_choice == '5':
        problem = inspyred.benchmarks.Schwefel(2)
        project_name = 'Schwefel'
    elif problem_choice == '6':
        problem = inspyred.benchmarks.Sphere(2)
        project_name = 'Sphere'
    elif problem_choice == '7':
        problem = inspyred.benchmarks.Kursawe(2)
        project_name = 'Kursawe'
    elif problem_choice == '8':
        points = [(110.0, 225.0), (161.0, 280.0), (325.0, 554.0), (490.0, 285.0),
              (157.0, 443.0), (283.0, 379.0), (397.0, 566.0), (306.0, 360.0),
              (343.0, 110.0), (552.0, 199.0)]
        weights = [[0 for _ in range(len(points))] for _ in range(len(points))]
        for i, p in enumerate(points):
            for j, q in enumerate(points):
                weights[i][j] = math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
        problem = inspyred.benchmarks.TSP(weights)
        project_name = 'TSP'
    elif problem_choice == '9':
        capacity = prng.randint(1,1000)
        items = []
        num_items = prng.randint(1,100)
        for i in range(0,num_items):
            items.append( (prng.randint(1,25), prng.randint(1,25)) )
        problem = inspyred.benchmarks.Knapsack(capacity, items)
        project_name = 'Knapsack'

    ea = inspyred.ec.GA(prng)
    #Can we make tanager file observer a class.
    ea.observer = tanager.tanager_file_observer
    ea.terminator = inspyred.ec.terminators.evaluation_termination
    final_pop = ea.evolve(generator=problem.generator,
                          evaluator=problem.evaluator,
                          pop_size=150,
                          bounder=problem.bounder,
                          maximize=problem.maximize,
                          max_evaluations=2500,
                          inheritance=True,
                          tanager_project_name=project_name)
    best = max(final_pop)
    print('Best Solution: \n{0}'.format(str(best)))