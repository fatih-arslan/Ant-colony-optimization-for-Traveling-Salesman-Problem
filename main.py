import numpy as np
import Ant as A
import time


def ant_colony_optimization(n_ants, n_iterations, alpha, beta, rho, Q, cities):
    n = len(cities)
    pheromone = np.ones((n, n)) # initialize pheromone trails to 1
    ants = [A.Ant(n, alpha, beta, pheromone, cities) for _ in range(n_ants)]
    best_distance = float('inf')
    best_route = None
    for i in range(n_iterations):
        for ant in ants:
            ant.reset()
            ant.run(np.random.randint(0, n))
            if ant.distance < best_distance:
                best_distance = ant.distance
                best_route = ant.tour
            ant.update_pheromone(Q)
        pheromone *= (1 - rho) # evaporate pheromones
        pheromone += rho*np.ones((n, n))*np.mean([ant.distance for ant in ants]) # global update
    return best_distance, best_route

n_ants = 20
n_iterations = 20
alpha = 2.5 # the parameter that controls the influence of the pheromone trail on the ant's decision-making process.
beta = 7 # the parameter that controls the influence of the distance between cities on the ant's decision-making process.
evaporation_rate = 0.8
Q = 100 # the parameter that controls the amount of pheromone that an ant deposits on the trail after completing a tour.
with open("files/tsp_5_1", "r") as file:
    n = int(file.readline().strip())
    cities = []
    for i in range(n):
        x, y = map(float, file.readline().split())
        cities.append((x, y))

start_time = time.time()
best_distance, best_tour = ant_colony_optimization(n_ants, n_iterations, alpha, beta, evaporation_rate, Q, cities)
end_time = time.time()

print("Optimal cost:", best_distance)
print("Optimal route", " ".join(map(str, best_tour)))
print(f"Time taken: {end_time - start_time:.2f} seconds")