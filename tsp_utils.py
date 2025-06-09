import random
import matplotlib.pyplot as plt
import time
import math

# Générer n villes aléatoires dans un carré de 100x100
def generer_villes(n, largeur=100, hauteur=100):
    villes = []
    for i in range(n):
        x = random.uniform(0, largeur)
        y = random.uniform(0, hauteur)
        villes.append((x, y))
    return villes


# Affichage
def afficher_villes(villes):
    xs, ys = zip(*villes)
    plt.figure(figsize=(6,6))
    plt.scatter(xs, ys, color='blue')
    for i, (x, y) in enumerate(villes):
        plt.text(x + 1, y + 1, str(i), fontsize=9)
    plt.title("Carte des villes")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.show()


def calculer_matrice_distances(villes):
    n = len(villes)
    distances = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                xi, yi = villes[i]
                xj, yj = villes[j]
                distances[i][j] = math.dist((xi, yi), (xj, yj))
    return distances

# Heuristique : Plus proche voisin
def nearest_neighbor(villes, distances):
    start_time = time.time()

    n = len(villes)
    visited = [False] * n
    chemin = [0]  # Commencer à la ville 0
    visited[0] = True
    total_distance = 0

    current = 0
    for _ in range(n - 1):
        next_city = None
        min_dist = float('inf')
        for j in range(n):
            if not visited[j] and distances[current][j] < min_dist:
                next_city = j
                min_dist = distances[current][j]
        chemin.append(next_city)
        total_distance += min_dist
        visited[next_city] = True
        current = next_city

    # Retour à la ville de départ
    total_distance += distances[current][0]
    chemin.append(0)

    execution_time = time.time() - start_time
    return chemin, total_distance, execution_time
