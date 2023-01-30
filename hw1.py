import numpy as np
import matplotlib.pyplot as plt
import math


def metric(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def calculate_length(route, cities):
    n = len(cities)
    L = 0
    for i in range(n - 1):
        L += metric(cities[route[i]], cities[route[i + 1]])
    L += metric(cities[route[-1]], cities[route[0]])
    return L


def generate_new_route(route):
    new_route = list(route)
    n = len(route)

    i = np.random.randint(n)
    j = np.random.randint(n)
    while i == j:
        j = np.random.randint(n)  # to ensure i != j

    if i > j:
        t = i
        i = j
        j = t
    if i != 0:
        new_route[i: j + 1] = new_route[j: i - 1: -1]
    else:
        new_route[i: j + 1] = new_route[j:: -1]

    return new_route


def get_prob(dL, T):
    return np.exp(-dL / T)


def is_transition(prob):
    return np.random.rand(1) <= prob


def decrease_temp(init_temp, k):
    return init_temp * 0.1 / k


def generate_init_route(cities):
    return [i for i in range(len(cities))]


def optimize_route(cities, init_temp, end_temp):
    n_cities = len(cities)
    route = generate_init_route(cities)

    cur_len = calculate_length(route, cities)
    print("Inital route length: ", cur_len)

    T = init_temp

    for k in range(1, 1000001):
        new_route = generate_new_route(route)
        new_len = calculate_length(new_route, cities)

        if new_len < cur_len:
            route = new_route
            cur_len = new_len
        else:
            p = get_prob(new_len - cur_len, T)
            if is_transition(p):
                route = new_route
                cur_len = new_len

        T = decrease_temp(init_temp, k)

        if T <= end_temp:
            break

        if k % 10000 == 0:
            print(int(k/10000), "%")

    print("Final route length: ", cur_len)
    return route


def simulated_annealing():
    n_cities = 100
    init_temp = 100
    end_temp = 0

    cities = np.random.rand(n_cities, 2) * 10
    plt.plot(cities[:, 0], cities[:, 1], "b-o")
    plt.title('Initial route')
    plt.show()

    route = optimize_route(cities, init_temp, end_temp)

    plt.plot(cities[route, 0], cities[route, 1], "g-o")
    plt.title('Final route')
    plt.show()


if __name__ == '__main__':
    simulated_annealing()
