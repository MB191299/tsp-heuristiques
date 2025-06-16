import random
import matplotlib.pyplot as plt
import time
import math
import heapq

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

# Heuristique d'Insertion
def insertion_heuristique(villes, distances):
    import time
    start_time = time.time()
    n = len(villes)

    non_visitees = list(range(n))
    tour = [0, 1, 0]  # On commence avec les villes 0 → 1 → 0
    non_visitees.remove(0)
    non_visitees.remove(1)

    while non_visitees:
        meilleur_cout = float('inf')
        meilleure_ville = None
        meilleure_position = None

        for ville in non_visitees:
            for i in range(1, len(tour)):
                a = tour[i - 1]
                b = tour[i]
                cout = distances[a][ville] + distances[ville][b] - distances[a][b]
                if cout < meilleur_cout:
                    meilleur_cout = cout
                    meilleure_ville = ville
                    meilleure_position = i

        tour.insert(meilleure_position, meilleure_ville)
        non_visitees.remove(meilleure_ville)

    # Calcul de la distance totale
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distances[tour[i]][tour[i + 1]]

    execution_time = time.time() - start_time
    return tour, total_distance, execution_time

# Comparaison avec Nearest Neighbor
def comparer_heuristiques(villes, distances):
    chemin_nn, dist_nn, t_nn = nearest_neighbor(villes, distances)
    chemin_ins, dist_ins, t_ins = insertion_heuristique(villes, distances)

    print("🔹 Nearest Neighbor")
    print(f"  Distance totale : {dist_nn:.2f}")
    print(f"  Temps d'exécution : {t_nn:.4f} s\n")

    print("🔹 Insertion Heuristique")
    print(f"  Distance totale : {dist_ins:.2f}")
    print(f"  Temps d'exécution : {t_ins:.4f} s\n")
    
    # Visualisation du chemin
def afficher_chemin(villes, chemin, titre="Circuit", couleur='blue', distance=None):
    xs = [villes[i][0] for i in chemin] + [villes[chemin[0]][0]]
    ys = [villes[i][1] for i in chemin] + [villes[chemin[0]][1]]

    plt.figure(figsize=(8, 6))
    plt.scatter(*zip(*villes), c='black', zorder=2)
    plt.plot(xs, ys, c=couleur, zorder=1, linewidth=2, marker='o', label="Chemin")

    for i, (x, y) in enumerate(villes):
        plt.text(x + 1, y + 1, str(i), fontsize=9)

    titre_complet = f"{titre} – Distance : {distance:.2f}" if distance else titre
    plt.title(titre_complet)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.axis("equal")
    plt.show()


    # Comparaison les heuristique en termes de distance totale, temps d'exécution et qualité 
import heapq

def mst_borne_inferieure(distances):
    """
    Calcule une borne inférieure pour le TSP via l'arbre couvrant minimal (MST).
    Utilise l’algorithme de Prim.
    """
    n = len(distances)
    visited = [False] * n
    min_edge = [float('inf')] * n
    min_edge[0] = 0
    heap = [(0, 0)]
    total = 0

    while heap:
        cout, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        total += cout

        for v in range(n):
            if not visited[v] and distances[u][v] < min_edge[v]:
                min_edge[v] = distances[u][v]
                heapq.heappush(heap, (distances[u][v], v))

    return total
