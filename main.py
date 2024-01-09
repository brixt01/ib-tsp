'''
Author: Ben Brixton
Last modified: 11/02/23
Description: Solve the travelling salesman problem using a genetic algorithm
'''

# Imports libraries, sets up turtle
import random
import matplotlib.pyplot as plt
import turtle as t
t.hideturtle()
t.speed(0)

# Gets user input
print("Number of cities: ")
n_cities = int(input())
print("Population size: ")
n_pop = int(input())
print("Number of generations: ")
n_gen = int(input())

# Gets algorithm choice
print("\nAlgorithm (1=Random, 2=OX, 3=PMX, 4=CX): ")
choice = int(input())
if choice == 1:
    algorithm = "Random"
elif choice == 2:
    algorithm = "OX"
elif choice == 3:
    algorithm = "PMX"
    print("PMX algorithm not implemented yet.")
elif choice == 4:
    algorithm = "CX"
    print("CX algorithm not implemented yet.")

# Gets other options
print("\nFastest? (1=T, 0=F): ")
fastest = bool(int(input()))
if fastest == False:
    print("Slow mode? (1=T, 0=F): ")
    slow = bool(int(input()))
    print("Draw mode? (1=T, 0=F): ")
    draw = bool(int(input()))
else: 
    slow = False
    draw = False

# Place cities randomly (x, y)
def placeCities(n_cities):
    cities = []
    for i in range(n_cities):
        cities.append([random.randint(0, 100), random.randint(0, 100)])
    return cities

# Draw cities with turtle
def drawCities(cities):
    t.penup()
    t.goto((cities[0][0]-50)*4, (cities[0][1]-50)*4)
    for count, city in enumerate(cities):
        t.goto((city[0]-50)*4, (city[1]-50)*4)
        t.write(count)

# Create initial population
def makePopulation(n_cities, n_pop):
    population = []
    for i in range(n_pop):
        population.append(random.sample(range(n_cities), n_cities))
    return population

# Calculate distance between two cities
def distance(city1, city2):
    return ((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)**0.5

# Calculate fitness of a member of the population (distance travelled)
def findFitness(member):
    total_distance = 0
    for i in range(len(member) - 1):
        total_distance += distance(cities[member[i]], cities[member[i+1]])
    return total_distance

# Evaluate fitness of entire population
def evaluate(population):
    fitnesses = []
    for member in population:
        fitnesses.append(findFitness(member))
    return fitnesses

# Sort population by fitness
def sort(population, fitness):
    population = [member for i, member in sorted(zip(fitness, population))]
    fitness = sorted(fitness)
    return population, fitness

# Draw tour with turtle
def drawTour(tour, cities):
    t.clear()
    t.penup()
    t.goto((cities[tour[0]][0]-50)*4, (cities[tour[0]][1]-50)*4)
    t.pendown()
    for i in range(0, len(tour)):
        t.goto((cities[tour[i]][0]-50)*4, (cities[tour[i]][1]-50)*4)
    drawCities(cities)

# Random algorithm
def rand(population, n_pop, n_cities):
    new_population = [population[0]]
    while len(new_population) < n_pop:
        new_population.append(random.sample(range(n_cities), n_cities))
    return new_population

# Order crossover algorithm
def OX(population, n_pop, n_cities):
    new_population = []
    for i in range(0, int(len(population)/4)):
        new_population.append(population[i])
    
    while len(new_population) < n_pop:
        # Choose two parents
        parent_1 = population[random.randint(0, n_pop-1)]
        parent_2 = population[random.randint(0, n_pop-1)]

        # Choose a random sequence length and starting point
        sequence_length = int(n_cities/2)
        starting_point = random.randint(0, n_cities-sequence_length)

        # Create blank child
        child = [-1] * n_cities

        # Copy sequence from parent 1 to child
        child[starting_point:starting_point+sequence_length] = parent_1[starting_point:starting_point+sequence_length]

        # Calculate where to start from in parent 2
        starting_point += sequence_length
        if starting_point >= n_cities:
            starting_point = 0

        # Add remaining cities from parent 2 to child
        parent_2_index = starting_point
        for i in range(0, n_cities-sequence_length):
            if starting_point+i >= n_cities:
                starting_point -= n_cities
            added = False
            while added == False:
                if parent_2_index >= n_cities:
                    parent_2_index -= n_cities
                if parent_2[parent_2_index] not in child:
                    child[starting_point+i] = parent_2[parent_2_index]
                    added = True
                else:
                    parent_2_index += 1
        # Add child
        new_population.append(child)
    return new_population

# Partially mapped crossover algorithm
def PMX(population, n_pop, n_cities):
    pass

# Cycle crossover algorithm
def CX(population, n_pop, n_cities):
    pass

# Plot fitnesses
def plotFitnesses(fitnesses):
    plt.plot(fitnesses)
    plt.ylabel('Fitness')
    plt.xlabel('Generation')
    plt.show()

# Create cities and initial population, draw cities
cities = placeCities(n_cities)
print("\nCities created...")
population = makePopulation(n_cities, n_pop)
print("Initial population created...")
drawCities(cities)
print("Cities drawn...")

print("\nPress enter to continue...")
input()

# Run algorithm
fitnesses = []
if fastest == False:
    print("Starting generation", 0, "...")
for generation in range(0, n_gen):

    fitness = evaluate(population)
    population, fitness = sort(population, fitness)

    if fastest == False:
        print("Population evaluated...")
        print("Best tour:", population[0], "with fitness", fitness[0])

    fitnesses.append(fitness[0])

    if draw == True:
        drawTour(population[0], cities)
        print("Showing best tour for generation", generation ,"...")

    if slow == True:
        print("\nPress enter to continue...")
        input()

    if fastest == False:
        print()
        print("Starting generation", generation+1, "...")
    
    if algorithm == "random":
        population = rand(population, n_pop, n_cities)
    elif algorithm == "OX":
        population = OX(population, n_pop, n_cities)
    elif algorithm == "PMX":
        population = PMX(population, n_pop, n_cities)
    elif algorithm == "CX":
        population = CX(population, n_pop, n_cities)
    if fastest == False:
        print("New population created...")

# Print best tour
print("After ", n_gen, " generations, the best tour found:", population[0], "with fitness", fitness[0])
drawTour(population[0], cities)
plotFitnesses(fitnesses)
t.done()