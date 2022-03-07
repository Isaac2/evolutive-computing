# Based on https://machinelearningmastery.com/simple-genetic-algorithm-from-scratch-in-python/
from numpy.random import randint
from numpy.random import rand
import math as math

def function_1(x):
    total = 0
    for i in range(0, 3):
        total += (x[0] - 2)**2
    return total

def function_2(x):
    total = 20 + x[0]**2 + x[1]**2 - 10*math.cos(2*math.pi*x[0]) - 10*math.cos(2*math.pi*x[1])
    return total

def function_3(x):
    total = -( (1 + math.cos(12*math.sqrt(x[0]**2 + x[1]**2)) / (0.5*(x[0]**2+x[1]**2) + 2)))
    return total

def decode(bounds, chromosomes, bitstring):
    #[0, 1]
    #01
    #Binary evaluation (01)

    decoded = list()
    largest = 2**chromosomes

    for i in range(len(bounds)):
        start = i * chromosomes
        end = (i+1) * chromosomes
        chromosomes_selected = bitstring[start:end]
        chars = ''.join([str(s) for s in chromosomes_selected])
        integer = int(chars, 2)

        value = bounds[i][0] + (integer/largest) * (bounds[i][1] - bounds[i][0])
        decoded.append(value)
    return decoded

def selection(elements, scores):
	selected_index = randint(len(elements))

	for i in randint(0, len(elements), 2):
		if scores[i] < scores[selected_index]:
			selected_index = i
	return elements[selected_index]

def crossover(parent1, parent2):
    '''
    Parents
    [0, 0, 0, 0]
    [1, 1, 1, 1]

    Child
    [0, 0, 0, 0]
    [0, 0, 0, 1]
    [0, 0, 1, 0]
        ...
    '''

    #Parent's chromosomes have the same size, so the sizes complement each other
    part = randint(1, len(parent1)-2)
    child1 = parent1[:part] + parent2[part:]
    child2 = parent2[:part] + parent1[part:]
    return [child1, child2]

def mutation(bitstring, mutation_rate):
	for i in range(len(bitstring)):
		if rand() < mutation_rate:
			bitstring[i] = 1 - bitstring[i]

def run(fx, bounds, chromosomes, iterations, population, mutation_rate):
    pop = [randint(0, 2, chromosomes*len(bounds)).tolist() for _ in range(population)]

    best = 0
    best_eval = fx(decode(bounds, chromosomes, pop[0]))
    for generation_index in range(iterations):
        decoded = [decode(bounds, chromosomes, p) for p in pop]
        scores = [fx(d) for d in decoded]

        #Evaluate each element in population in current generation_index
        #Select the best elements to repopulate
        for i in range(population):
            if scores[i] < best_eval:
                best = pop[i]
                best_eval = scores[i]
                print("New best found in generation #%d, coordinates: (%s): %f" % (generation_index, decoded[i], best_eval))
        selected = [selection(pop, scores) for _ in range(population)]

        #Repopulate crossing best elements in current generation
        children = list()
        for i in range(0, population, 2):
            parent1 = selected[i]
            parent2 = selected[i+1]

            for child in crossover(parent1, parent2):
                mutation(child, mutation_rate)
                children.append(child)

        pop = children
    return [best, best_eval]
 
#########################################
## PARAMÉTROS
#########################################
lower_limit = -2
upper_limit = 2
bounds = [[lower_limit, upper_limit], [lower_limit, upper_limit]]

iterations = 100
chromosomes = 100 #D
population = 100

mutation_rate = 1.0 / (float(chromosomes) * len(bounds))
#best, score = run(function_1, bounds, chromosomes, iterations, population, mutation_rate)
#decoded = decode(bounds, chromosomes, best)
#print("\nFinished first function")
#print("Minimum value found in (%s): %f" % (decoded, score))

lower_limit = -5
upper_limit = 5
chromosomes = 5
bounds = [[lower_limit, upper_limit], [lower_limit, upper_limit]]
#best, score = run(function_2, bounds, chromosomes, iterations, population, mutation_rate)
#decoded = decode(bounds, chromosomes, best)
#print("\nFinished second RASTRIGIN function")
#print("Minimum value found in (%s): %f" % (decoded, score))

lower_limit = -5
upper_limit = 5
chromosomes = 100
bounds = [[lower_limit, upper_limit], [lower_limit, upper_limit]]
best, score = run(function_3, bounds, chromosomes, iterations, population, mutation_rate)
decoded = decode(bounds, chromosomes, best)
print("\nFinished third function")
print("Minimum value found in (%s): %f" % (decoded, score))