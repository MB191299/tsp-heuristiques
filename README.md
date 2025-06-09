# TSP - Heuristiques de résolution du Problème du Voyageur de Commerce

Ce projet implémente des **heuristiques pour résoudre le Problème du Voyageur de Commerce (TSP)** en Python, dans le cadre d’un projet scolaire.

## Objectifs

- Générer aléatoirement des villes (coordonnées 2D)
- Calculer la matrice de distances entre les villes
- Implémenter des heuristiques de résolution (nearest neighbor, etc.)
- Visualiser les résultats (trajets, distances, temps d’exécution)
- (Bonus) Charger des fichiers CSV de villes

---

## Organisation du projet

### Fichiers principaux

- `tsp_utils.py` : fonctions utilitaires
  - `generer_villes(n)`
  - `afficher_villes(villes)`
  - `calculer_matrice_distances(villes)`
  - `nearest_neighbor(villes, distances)`
- `tsp.ipynb` : notebook principal pour exécuter, tester et visualiser

---

## Heuristique 1 : Plus Proche Voisin (Nearest Neighbor)

- Approche gloutonne qui choisit à chaque étape la ville la plus proche
- Retourne le chemin complet + distance totale + temps d’exécution

#### Exemple d'utilisation :
```python
from tsp_utils import generer_villes, calculer_matrice_distances, nearest_neighbor

villes = generer_villes(20)
distances = calculer_matrice_distances(villes)
chemin, distance_totale, temps = nearest_neighbor(villes, distances)
print(f"Chemin : {chemin}")
print(f"Distance totale : {distance_totale:.2f}")
print(f"Temps d'exécution : {temps:.4f} secondes")
# tsp-heuristiques
Projet de résolution heuristique du problème du voyageur de commerce
