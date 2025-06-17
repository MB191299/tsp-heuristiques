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

```

---

## **Heuristique 2 : Insertion** 
Cette seconde heuristique repose sur une stratégie incrémentale : on commence avec un sous-tour réduit (par exemple 2 ou 3 villes), puis on insère les autres villes une à une à l’endroit qui minimise l’augmentation de la distance totale du chemin.

### Objectif
Trouver un chemin plus optimisé que le Plus Proche Voisin (NN), en évitant les choix trop locaux dès le départ.

### Fonction principale
```python
insertion_heuristique(villes, distances)
```
### Fonctionnement
- Initialiser un cycle de 2 ou 3 villes.
- À chaque itération, choisir une ville non encore insérée.
- L’ajouter dans la position du tour actuel qui augmente le moins la distance totale.
- Répéter jusqu’à avoir un tour complet.

### Résultats retournés
- `chemin` : liste des indices des villes dans l’ordre visité
- `distance_totale` : longueur totale du chemin
- `temps_execution` : durée du calcul

### Exemple d'utilisation
```python
from tsp_utils import generer_villes, calculer_matrice_distances, insertion_heuristique

villes = generer_villes(20)
distances = calculer_matrice_distances(villes)
chemin, distance_totale, temps = insertion_heuristique(villes, distances)

print(f"Chemin : {chemin}")
print(f"Distance totale : {distance_totale:.2f}")
print(f"Temps d'exécution : {temps:.4f} secondes")
```
### Comparaison
Cette heuristique a été testée avec les mêmes ensembles de villes que `nearest_neighbor`, et les performances ont été comparées en termes de:
- Distance totale parcourue
- Temps d’exécution

## 📈 Comparaison des Heuristiques

| Heuristique        | Distance (ex. 20 villes) | Temps (s) | Remarques                      |
|--------------------|--------------------------|-----------|--------------------------------|
| Plus Proche Voisin | 168.2                    | 0.0012    | Rapide, mais solutions locales |
| Insertion          | 150.6                    | 0.0021    | Mieux optimisé globalement     |


## Visualisation

Les fonctions de visualisation permettent de tracer les villes et les chemins trouvés par chaque heuristique à l’aide de `matplotlib`.

### Fonction : `afficher_chemin(villes, chemin, titre, couleur, distance)`
- Affiche les villes en 2D
- Trace le chemin parcouru dans l’ordre
- Affiche la distance totale dans le titre

#### Exemple :
```python
from tsp_utils import afficher_chemin
afficher_chemin(villes, chemin, titre="Nearest Neighbor", distance=distance_totale)
