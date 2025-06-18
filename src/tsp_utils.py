import random
import matplotlib.pyplot as plt
import time
import math
import heapq

def generer_villes(n, largeur=100, hauteur=100):
    """
    Génère aléatoirement n villes dans un rectangle de dimensions données.

    Paramètres :
    - n (int) : nombre de villes à générer.
    - largeur (float) : largeur maximale du plan (par défaut 100).
    - hauteur (float) : hauteur maximale du plan (par défaut 100).

    Retour :
    - List[Tuple[float, float]] : liste des coordonnées (x, y) des villes générées.
    """
    villes = []
    for i in range(n):
        x = random.uniform(0, largeur)
        y = random.uniform(0, hauteur)
        villes.append((x, y))
    return villes


def afficher_villes(villes):
    """
    Affiche les villes sur un plan 2D avec leurs indices.

    Paramètres :
    - villes (List[Tuple[float, float]]) : liste des coordonnées des villes.
    
    Retour :
    - Aucun (affichage graphique via matplotlib).
    """
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
    """
    Calcule la matrice des distances euclidiennes entre chaque paire de villes.

    Paramètres :
    - villes (List[Tuple[float, float]]) : liste des coordonnées des villes.

    Retour :
    - List[List[float]] : matrice des distances entre les villes.
    """
    n = len(villes)
    distances = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                xi, yi = villes[i]
                xj, yj = villes[j]
                distances[i][j] = math.dist((xi, yi), (xj, yj))
    return distances

def nearest_neighbor(villes, distances):
    """
    Résout le problème du TSP à l’aide de l’algorithme du plus proche voisin.

    Paramètres :
    - villes (List[Tuple[float, float]]) : liste des coordonnées des villes.
    - distances (List[List[float]]) : matrice des distances entre les villes.

    Retour :
    - chemin (List[int]) : ordre des villes visitées (terminé par un retour au départ).
    - total_distance (float) : distance totale du circuit.
    - execution_time (float) : durée d’exécution de l’algorithme en secondes.
    """
    start_time = time.time()

    n = len(villes)
    visited = [False] * n
    chemin = [0]  # Commence à la ville 0
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

def insertion_heuristique(villes, distances):
    """
    Résout le problème du TSP en utilisant l’heuristique d’insertion.

    Paramètres :
    - villes (List[Tuple[float, float]]) : liste des coordonnées des villes.
    - distances (List[List[float]]) : matrice des distances entre les villes.

    Retour :
    - tour (List[int]) : ordre des villes visitées, commençant et terminant à la même ville.
    - total_distance (float) : distance totale du circuit.
    - execution_time (float) : durée d’exécution de l’algorithme en secondes.
    """
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

def comparer_heuristiques(villes, distances):
    """
    Compare les deux heuristiques (Nearest Neighbor et Insertion) sur un même ensemble de villes.

    Affiche pour chaque méthode :
    - la distance totale du circuit
    - le temps d'exécution
    - le ratio par rapport à une borne inférieure estimée (via MST)

    Paramètres :
    - villes (List[Tuple[float, float]]) : liste des coordonnées des villes.
    - distances (List[List[float]]) : matrice des distances.

    Retour :
    - Aucun (affiche les résultats et les tracés).
    """
     # Exécution des heuristiques
    chemin_nn, dist_nn, t_nn = nearest_neighbor(villes, distances)
    chemin_ins, dist_ins, t_ins = insertion_heuristique(villes, distances)

    # Calcul de la borne inférieure avec l'arbre couvrant minimal (MST)
    borne = mst_borne_inferieure(distances)

    # Calcul des ratios distance / borne inférieure
    qualite_nn = dist_nn / borne
    qualite_ins = dist_ins / borne

    # Affichage des résultats
    print("🔹 Nearest Neighbor")
    print(f"  Distance totale : {dist_nn:.2f}")
    print(f"  Temps d'exécution : {t_nn:.4f} s\n")
    print(f"  ➤ Ratio distance / borne : {qualite_nn:.2f}\n")

    print("🔹 Insertion Heuristique")
    print(f"  Distance totale : {dist_ins:.2f}")
    print(f"  Temps d'exécution : {t_ins:.4f} s\n")
    print(f"  ➤ Ratio distance / borne : {qualite_ins:.2f}\n")

    print(f" Borne inférieure estimée (MST) : {borne:.2f}")

    # Visualisation du chemin
    afficher_chemin(villes, chemin_nn, titre="Nearest Neighbor", couleur='blue', distance=dist_nn)
    afficher_chemin(villes, chemin_ins, titre="Heuristique d'Insertion", couleur='green', distance=dist_ins)
    
def afficher_chemin(villes, chemin, titre="Circuit", couleur='blue', distance=None):
    """
    Affiche un chemin TSP sur la carte des villes.

    Paramètres :
    - villes (List[Tuple[float, float]]) : coordonnées des villes.
    - chemin (List[int]) : ordre des villes visitées.
    - titre (str) : titre du graphique (facultatif).
    - couleur (str) : couleur de la ligne du chemin.
    - distance (float) : distance totale affichée dans le titre (facultatif).

    Retour :
    - Aucun (affichage graphique via matplotlib).
    """
    xs = [villes[i][0] for i in chemin]
    ys = [villes[i][1] for i in chemin]

    plt.figure(figsize=(8, 6))
    plt.scatter(*zip(*villes), c='black', zorder=2)
    plt.plot(xs, ys, c=couleur, zorder=1, linewidth=2, label="Chemin")

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

def mst_borne_inferieure(distances):
    """
    Calcule une borne inférieure pour le TSP à l'aide de l'arbre couvrant minimal (MST) via l’algorithme de Prim.

    Paramètres :
    - distances (List[List[float]]) : matrice des distances entre les villes.

    Retour :
    - total (float) : poids total de l’arbre couvrant minimal (borne inférieure pour le TSP).
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

# ================================
# Exécution principale
# ================================
if __name__ == "__main__":
    villes = generer_villes(15)
    afficher_villes(villes)
    distances = calculer_matrice_distances(villes)
    comparer_heuristiques(villes, distances)