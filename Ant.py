import math
import numpy as np

class Ant:
    def __init__(self, n, alpha, beta, pheromone, cities):
        self.n = n  # number of cities
        self.alpha = alpha  # pheromone trail exponent
        self.beta = beta  # heuristic information exponent
        self.pheromone = pheromone  # pheromone trail matrix
        self.cities = cities  # list of cities
        self.visited = [False] * n  # list of visited cities
        self.tour = []  # list of visited cities in order
        self.distance = 0  # total distance of the tour

    def get_distance(self, city1, city2):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
    def choose_next_city(self, current_city):
        unvisited_cities = [i for i in range(self.n) if not self.visited[i]]
        probabilities = [0] * self.n
        total_prob = 0
        for i in unvisited_cities:
            probabilities[i] = self.pheromone[current_city][i] ** self.alpha * (
                        1 / self.get_distance(self.cities[current_city], self.cities[i])) ** self.beta
            total_prob += probabilities[i]
        if total_prob == 0:
            return None
        probabilities = [p / total_prob for p in probabilities]
        next_city = np.random.choice(self.n, p=probabilities)
        return next_city

    def tour_length(self):
        for i in range(self.n):
            self.distance += self.get_distance(self.cities[self.tour[i]], self.cities[self.tour[(i + 1) % self.n]])

    def run(self, start_city):
        self.tour = [start_city]
        self.visited[start_city] = True
        current_city = start_city
        for i in range(self.n - 1):
            next_city = self.choose_next_city(current_city)
            if next_city is None:
                break
            self.tour.append(next_city)
            self.visited[next_city] = True
            current_city = next_city
        self.tour.append(start_city)
        self.tour_length()

    def update_pheromone(self, Q):
        for i in range(self.n):
            j = (i + 1) % self.n
            self.pheromone[self.tour[i]][self.tour[j]] += Q / self.distance

    def reset(self):
        self.visited = [False] * self.n
        self.tour = []
        self.distance = 0
