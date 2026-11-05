# 🍕 Plato's Pizza : analyse des ventes 2015

Auteur : Zohair (formation Data Analyst, Simplon Lyon)

Application en ligne : https://pizza-zohair.streamlit.app/

## Question métier

Quand, quoi et combien vend Plato's Pizza, et où peut-elle agir pour vendre plus ou mieux s'organiser ?

Chaque équipe a sa propre question :
- **Direction** : comment évolue le chiffre d'affaires ? Quelles catégories et quelles tailles rapportent le plus ?
- **Planning** : à quels jours et à quelles heures faut-il renforcer l'équipe ?
- **Stock et achats** : quels ingrédients commander en priorité ? Quelles pizzas se vendent peu ?
- **Marketing** : comment augmenter le panier moyen ? Quelles pizzas mettre en avant ?

## Données

4 fichiers CSV (Pizza Place Sales, année 2015), rangés dans `data/` :

| Fichier | Contenu | Lignes |
|---|---|---|
| `orders.csv` | une commande : date et heure | 21350 |
| `order_details.csv` | une pizza (type + taille) dans une commande, avec sa quantité | 48620 |
| `pizzas.csv` | une pizza dans une taille, avec son prix | 96 |
| `pizza_types.csv` | un type de pizza : nom, catégorie, ingrédients | 32 |

`pizza_types.csv` est encodé en `cp1252` (Windows), pas en UTF-8.

## Démarche

1. **Cadrage** : question métier, unité d'analyse, indicateurs.
2. **Exploration** des CSV avec pandas (`01_exploration.ipynb`) : types, valeurs manquantes, doublons, liens entre tables, période. Aucune ligne supprimée.
3. **Base SQL** (`02_creation_base.ipynb` + `sql/00_creation_tables.sql`) : 4 tables SQLite avec clés primaires et étrangères, chargement des CSV, contrôles du nombre de lignes et de la jointure.
4. **Requêtes SQL** et **analyse Python** (`03_analyse.ipynb`) : chaque requête est lancée avec `pd.read_sql`, suivie d'un graphique et d'une observation.
5. **Application Streamlit** (`app.py`) : elle lit la base `pizza.db`, jamais les CSV.

## Organisation du dossier

```
pizza-streamlit/
  data/                      les 4 CSV
  sql/
    00_creation_tables.sql   création des 4 tables (clés primaires et étrangères)
  01_exploration.ipynb       exploration des CSV
  02_creation_base.ipynb     création et chargement de pizza.db + contrôles
  03_analyse.ipynb           15 analyses SQL + graphiques + conclusion
  pizza.db                   base SQLite
  app.py                     application Streamlit
  .streamlit/config.toml     couleurs de l'application
  requirements.txt           bibliothèques Python
  README.md
```

## Installation

```
git clone https://github.com/Zohair69/pizza-streamlit.git
cd pizza-streamlit
python -m pip install -r requirements.txt
```

Avec Anaconda, ouvrir l'Anaconda Prompt et installer ce qui manque avec `conda install streamlit plotly`.

## Recréer la base

La base `pizza.db` est déjà dans le dépôt. Pour la recréer à partir des CSV, ouvrir `02_creation_base.ipynb` dans Jupyter et lancer toutes les cellules (Kernel > Restart Kernel and Run All Cells).

## Lancer l'application

```
python -m streamlit run app.py
```

L'application s'ouvre dans le navigateur (http://localhost:8501). Elle contient 3 rubriques :
1. **La question et la démarche** : question métier, questions de chaque équipe, étapes suivies.
2. **Tableau de bord** : filtres (période, catégorie, taille), indicateurs clés et graphiques interactifs, avec un onglet par équipe.
3. **Recommandations et limites** : constats clés calculés en SQL, propositions et limites.

## Principaux résultats (année 2015)

- Chiffre d'affaires de 817860.05, avec 21350 commandes et 49574 pizzas vendues. Panier moyen : 38.31.
- Deux pics par jour : le midi (12h et 13h) et le début de soirée (17h et 18h). Le vendredi est le jour le plus fort (70.8 commandes par jour ouvert).
- 38.0 % des commandes ne contiennent qu'une seule pizza.
- Les commandes de 10 pizzas ou plus représentent 1.6 % des commandes, mais 8.7 % du chiffre d'affaires.
- La taille L pèse 45.9 % du chiffre d'affaires. Les tailles XL et XXL pèsent très peu.

## Limites

- Une seule année de données (2015).
- Pas de coûts, donc pas de marge.
- Pas d'identifiant client ni de canal de vente.
- La monnaie n'est pas précisée.
- La liste d'ingrédients ne donne pas les quantités.
- 7 jours sans commande dans l'année (fermetures probables).
