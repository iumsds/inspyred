import sys
sys.path.append("../inspyred/inspyred/")
import ec
import inspyred
from random import Random
import time
import math
import os

def ensure_file(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    elif os.path.exists(file_path):             # backup previous file
        os.rename(file_path, f"{file_path}_{time.strftime('%m%d%Y_%H%M%S')}")

    tanager_file = open(file_path, 'w')     #open the file
    return tanager_file


def get_file(project_name, file_name, header_row):
    """
    Create the file and write the header row.
    :param project_name:
    :param file_name:
    :param header_row:
    :return:
    """
    file_name = f'./tanager_data/{project_name}/{file_name}'
    tanager_data_file = ensure_file(file_name)
    if header_row:
        tanager_data_file.write(header_row)     #write the header row.

    return tanager_data_file

def tanager_file_observer(population, num_generations, num_evaluations, args):
    """Print the output of the evolutionary computation to a file.
    """
    if 'family_tree' not in args:
        args['family_tree'] = {}

    if 'tanager_project_name' in args:
        project_name = args['tanager_project_name']
    else:
        project_name = time.strftime('%m%d%Y_%H%M%S')
        args['tanager_project_name'] = project_name

    if 'statistics_file' in args:     #prepare stats file.
        statistics_file = args['statistics_file']
    else:
        header_row = "num_generations,population_length,worst_fit,best_fit,median_fit,average_fit,std_fit,best_fit_candidate_hash\n"
        statistics_file = get_file(project_name, 'tanager-statistics-file.csv', header_row)
        args['statistics_file'] = statistics_file

    if 'individuals_file' in args:     #prepare stats file.
        individuals_file = args['individuals_file']
    else:
        header_row = "generation,i,fitness,hash,mom_hash,dad_hash,values\n"
        individuals_file = get_file(project_name, 'tanager-individuals-file.csv', header_row)
        args['individuals_file'] = individuals_file

    # try:
    #     statistics_file = args['statistics_file']
    # except KeyError:
    #     statistics_file = open('tanager-statistics-file-{0}.csv'.format(time.strftime('%m%d%Y-%H%M%S')), 'w')
    #     statistics_file.write("num_generations,population_length,worst_fit,best_fit,median_fit,average_fit,std_fit,best_fit_candidate_hash\n")
    #     args['statistics_file'] = statistics_file
    # try:
    #     individuals_file = args['individuals_file']
    # except KeyError:
    #     individuals_file = open('tanager-individuals-file-{}.csv'.format(time.strftime('%m%d%Y-%H%M%S')), 'w')
    #     individuals_file.write("generation,i,fitness,hash,mom_hash,dad_hash,values\n")
    #     args['individuals_file'] = individuals_file

    stats = inspyred.ec.analysis.fitness_statistics(population)
    worst_fit = stats['worst']
    best_fit = stats['best']
    avg_fit = stats['mean']
    med_fit = stats['median']
    std_fit = stats['std']

    best_fitness_candidate = None
    best_fitness_candidate_i = -1
    for i, p in enumerate(population):
        p_hash = hash(tuple(p.candidate))
        try:
            parents = args['family_tree'][p_hash]
        except KeyError as error:
            parents = {"mom": 0, "dad": 0}
        candidate_value = str(p.candidate).replace(',',' ').replace('[','').replace(']','')
        individuals_file.write(f"{num_generations},{i},{p.fitness},{p_hash},{parents['mom']},{parents['dad']},{candidate_value}\n")
        #individuals_file.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(num_generations, i, p.fitness, p_hash, parents['mom'], parents['dad'], str(p.candidate).replace(',',' ').replace('[','').replace(']','')))
        if p.fitness == best_fit:
            best_fitness_candidate = p.candidate
            best_fitness_candidate_i = i
    statistics_file.write(f"{num_generations},{len(population)},{worst_fit},{best_fit},{med_fit},{avg_fit},{std_fit},{best_fitness_candidate_i}\n")
    #statistics_file.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(num_generations, len(population), worst_fit, best_fit, med_fit, avg_fit, std_fit, hash(tuple(best_fitness_candidate))))

    statistics_file.flush()
    individuals_file.flush()

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
    ea.observer = tanager_file_observer
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