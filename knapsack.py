import random

num_items = 30
pop_size = 50

#Random weights and values for 30 items
values = [random.randint(0, 30) for x in range (0, num_items)]
weights = [random.randint(0, 30) for x in range (0, num_items)]

capacity = 10 * num_items
num_gens = 200


#Calculate how fit a chromosome is
def fitness(chromosome):
	total_val = 0
	total_weight = 0
	for index, i in enumerate(chromosome):
		if i == 1:		
			total_val += values[index]
			total_weight += weights[index]

	if total_weight > capacity:
		return 0
	else:
		return total_val


#Make a list of 50 unique chromosomes    
def create_pop():
	population = [[random.randint(0,1) for x in range (0, num_items)] for x in range (0, pop_size)]
	return population


#Find the total fitness of a population
def total_fitness(population):
	total = 0
	for chromosome in population:
		total += fitness(chromosome)
	return total	


#Calculate the highest value and the average value of fitness in a population
def fitness_info(population):
	highest_val = 0
	total_val = 0
	for chromosome in population:
		total_val += fitness(chromosome)
		if fitness(chromosome) > highest_val:
			highest_val = fitness(chromosome)
	average = total_val / len(population)
	return highest_val, average


#Return the chromosome with the highest fitness in a population	
def highest_chromosome(population):
        highest_val = 0
	best_chrom = 0
        for chromosome in population:
                if fitness(chromosome) > highest_val:
                        highest_val = fitness(chromosome)
			best_chrom = chromosome
        return best_chrom


#Use a weighted random selection method to chose fit parents
def weighted_random_choice(population):
    max_fit = total_fitness(population) 
    pick = random.uniform(0, max_fit)
    current = 0
    for chromosome in population:
        current += fitness(chromosome)
        if current > pick:
            return chromosome


#create two children with random crossover between two parents
def one_point_crossover(parent1, parent2):
	crossover_point = random.randint(0, len(parent1)-1)
	child1 = parent1[:crossover_point]+parent2[crossover_point:]
   	child2 = parent2[:crossover_point] + parent1[crossover_point:]
	return child1, child2


#Mutate the genes in a child 
def mutate(child):
	mutation_rate = 0.05
	for gene in child:
		pick = random.uniform(0, 1)
		if pick <= mutation_rate:
			if gene == 1:
				gene = 0
			else:
				gene = 1
	return child


#Add the top 10% of parents to the new population
def top_pop(population):
	population = sorted(population, key=lambda x: fitness(x), reverse=True)
	parent_length = int(0.1*len(population))
	parents = population[:parent_length]
	return parents


def main():
	population = create_pop()
	generation = 0
	start_pop = population 
        while(generation < num_gens): 
		new_population = top_pop(population)
		
		#Add children to the newest generation
		while len(new_population) < len(population):
			parent_1 = weighted_random_choice(population)
			parent_2 = weighted_random_choice(population)
			child1, child2 = one_point_crossover(parent_1, parent_2)
			new_population += [mutate(child1)]
			new_population += [mutate(child2)]

		population = new_population
		generation += 1
		print("Average Fitness: " + str(fitness_info(population)[1]))

	print("Weights: " + str(weights))
	print("Values: " + str(values))
	print("Best Chromosome: " + str(highest_chromosome(population)))
	print("Starting best chromosome: " + str(highest_chromosome(start_pop)))	
	print("Starting best: " + str(fitness_info(start_pop)[0]))
	print("Number of Generations: " + str(generation))
if __name__ == "__main__":
	main()
