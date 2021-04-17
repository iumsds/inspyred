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