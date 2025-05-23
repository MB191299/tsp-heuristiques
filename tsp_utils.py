import random
import matplotlib.pyplot as plt

# Générer n villes aléatoires dans un carré de 100x100
def generer_villes(n, largeur=100, hauteur=100):
    villes = []
    for i in range(n):
        x = random.uniform(0, largeur)
        y = random.uniform(0, hauteur)
        villes.append((x, y))
    return villes

# Exemple : générer 10 villes
villes = generer_villes(10)

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

afficher_villes(villes)

