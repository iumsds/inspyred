import sys
sys.path.append("../inspyred/inspyred/")
import ec
import inspyred
from random import Random
import time

def tanager_file_observer(population, num_generations, num_evaluations, args):
    """Print the output of the evolutionary computation to a file.
    """
    if 'family_tree' not in args:
        args['family_tree'] = {}
    
    try:
        statistics_file = args['statistics_file']
    except KeyError:
        statistics_file = open('tanager-statistics-file-{0}.csv'.format(time.strftime('%m%d%Y-%H%M%S')), 'w')
        statistics_file.write("num_generations,population_length,worst_fit,best_fit,median_fit,average_fit,std_fit,best_fit_candidate_hash\n")
        args['statistics_file'] = statistics_file
    try:
        individuals_file = args['individuals_file']
    except KeyError:
        individuals_file = open('tanager-individuals-file-{}.csv'.format(time.strftime('%m%d%Y-%H%M%S')), 'w')
        individuals_file.write("generation,i,fitness,hash,mom_hash,dad_hash,values\n")
        args['individuals_file'] = individuals_file

    stats = inspyred.ec.analysis.fitness_statistics(population)
    worst_fit = stats['worst']
    best_fit = stats['best']
    avg_fit = stats['mean']
    med_fit = stats['median']
    std_fit = stats['std']

    best_fitness_candidate = None
    for i, p in enumerate(population):
        p_hash = hash(tuple(p.candidate))
        parents = args['family_tree'].pop(p_hash, {"mom": 0, "dad": 0})
        individuals_file.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(num_generations, i, p.fitness, p_hash, parents['mom'], parents['dad'], str(p.candidate).replace(',',' ').replace('[','').replace(']','')))
        if p.fitness == best_fit:
            best_fitness_candidate = p.candidate
    statistics_file.write('{0},{1},{2},{3},{4},{5},{6},{7}\n'.format(num_generations, len(population), worst_fit, best_fit, med_fit, avg_fit, std_fit, hash(tuple(best_fitness_candidate))))
    
    
    statistics_file.flush()
    individuals_file.flush()


class TanagerEvolve(ec.EvolutionaryComputation):

    def __init__(self, random):
        EvolutionaryComputation.__init__(self, random)
        self.selector = selectors.rank_selection
        self.variator = [variators.n_point_crossover, variators.bit_flip_mutation]
        self.replacer = self._replacer_with_inheritance(replacers.generational_replacement)
    
    def evolve(self, generator, evaluator, pop_size=100, seeds=None, maximize=True, bounder=None, **args):
        args.setdefault('num_selected', pop_size)
        return EvolutionaryComputation.evolve(self, generator, evaluator, pop_size, seeds, maximize, bounder, **args)
    
    
    
if __name__ == '__main__':
    prng = Random()
    prng.seed(time())

    problem = inspyred.benchmarks.Rastrigin(2)
    ea = inspyred.ec.GA(prng)
    ea.observer = tanager_file_observer
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
