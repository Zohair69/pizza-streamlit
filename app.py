# Application Streamlit Plato's Pizza
# Auteur : Zohair
# Trois rubriques : 1. la question métier et la démarche, 2. le tableau de bord, 3. les recommandations.
# Toutes les données viennent de la base SQLite pizza.db (jamais des CSV).

import datetime
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Plato's Pizza", page_icon="🍕", layout="wide")

# ---------- Style "pizzeria" : fond crème, couleurs pâte / fromage / croûte ----------
st.markdown("""
<style>
h1, h2, h3 { color: #6B3E1D; }
.bandeau { background: linear-gradient(90deg, #E8871E, #F4C542); padding: 24px 32px; border-radius: 18px;
           color: white; margin-bottom: 20px; }
.bandeau h1 { color: white; margin: 0; font-size: 2.4rem; }
.bandeau p { margin: 4px 0 0 0; font-size: 1.1rem; }
.carte { background-color: white; border-left: 8px solid #E8871E; border-radius: 12px; padding: 16px 20px;
         margin-bottom: 14px; box-shadow: 0 2px 6px rgba(107, 62, 29, 0.12); color: #3B2A1A; }
.carte h4 { color: #6B3E1D; margin: 0 0 6px 0; }
.etape { background-color: white; border-top: 6px solid #E8871E; border-radius: 12px; padding: 12px;
         text-align: center; min-height: 190px; box-shadow: 0 2px 6px rgba(107, 62, 29, 0.12); color: #3B2A1A; }
.etape .icone { font-size: 2rem; }
[data-testid="stMetric"] { background-color: white; border-radius: 12px; padding: 12px 16px;
                           box-shadow: 0 2px 6px rgba(107, 62, 29, 0.12); }
</style>
""", unsafe_allow_html=True)

PALETTE = ["#E8871E", "#6B3E1D", "#F4C542", "steelblue", "purple", "grey"]   # orange, brun, jaune fromage...
JOURS = ["dim", "lun", "mar", "mer", "jeu", "ven", "sam"]   # strftime('%w') : 0 = dimanche


def bandeau(titre, sous_titre):
    """Affiche un bandeau orange en haut de la page."""
    st.markdown(f'<div class="bandeau"><h1>{titre}</h1><p>{sous_titre}</p></div>', unsafe_allow_html=True)


def carte(titre, texte):
    """Affiche un encadré blanc avec un titre et un texte."""
    st.markdown(f'<div class="carte"><h4>{titre}</h4>{texte}</div>', unsafe_allow_html=True)


def joli(fig):
    """Met le même style à tous les graphiques plotly."""
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#3B2A1A")
    if fig.layout.xaxis.title.text:   # enlève les _ des titres d'axes : "chiffre_affaires" -> "chiffre affaires"
        fig.update_xaxes(title=fig.layout.xaxis.title.text.replace("_", " "))
        fig.update_yaxes(title=fig.layout.yaxis.title.text.replace("_", " "))
    st.plotly_chart(fig)


# ---------- Connexion à la base ----------
con = sqlite3.connect("pizza.db")

# ---------- Menu des rubriques ----------
st.sidebar.markdown("# 🍕 Plato's Pizza")
rubrique = st.sidebar.radio("Rubrique", ["1. La question et la démarche",
                                         "2. Tableau de bord",
                                         "3. Recommandations et limites"])
st.sidebar.caption("Auteur : Zohair")

# =====================================================================
# RUBRIQUE 1 : la question métier et la démarche suivie
# =====================================================================
if rubrique == "1. La question et la démarche":
    bandeau("🍕 Plato's Pizza", "Comment vendre plus, et mieux s'organiser, à partir des ventes 2015 ?")

    st.header("La question principale")
    carte("Quand, quoi et combien vend Plato's Pizza, et où peut-elle agir ?",
          "Le gérant dispose d'une année de commandes. Il veut savoir ce qui marche, à quels moments, "
          "et ce qu'il peut changer pour augmenter son chiffre d'affaires.")

    st.header("Les questions de chaque équipe")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        carte("📈 Direction", "Comment évolue le chiffre d'affaires ? Quelles catégories et quelles tailles rapportent le plus ?")
    with col2:
        carte("👩‍🍳 Planning", "À quels jours et à quelles heures faut-il renforcer l'équipe en cuisine ?")
    with col3:
        carte("📦 Stock et achats", "Quels ingrédients commander en priorité ? Quelles pizzas se vendent peu ?")
    with col4:
        carte("📣 Marketing", "Comment augmenter le panier moyen ? Quelles pizzas mettre en avant ?")

    st.header("La démarche suivie")
    etapes = [
        ("🎯", "1. Cadrage", "Question métier, unité d'analyse, indicateurs"),
        ("🔍", "2. Exploration", "4 CSV lus avec pandas : types, manquants, doublons, liens entre tables"),
        ("🗄️", "3. Base SQL", "Script SQL (clés primaires et étrangères), chargement dans SQLite, contrôles"),
        ("🧮", "4. Requêtes SQL", "Indicateurs, temps, produits, catégories, tailles, ingrédients"),
        ("📊", "5. Analyse Python", "pd.read_sql, graphiques, observations chiffrées"),
        ("🍕", "6. Application", "Streamlit lit la base SQL, avec des filtres"),
        ("💡", "7. Recommandations", "Propositions, conclusion et limites"),
    ]
    colonnes = st.columns(len(etapes))
    for colonne, (icone, titre, texte) in zip(colonnes, etapes):
        colonne.markdown(f'<div class="etape"><div class="icone">{icone}</div><b>{titre}</b><br><small>{texte}</small></div>',
                         unsafe_allow_html=True)

    st.header("Les données")
    tailles = pd.read_sql("""SELECT 'orders' AS table_sql, COUNT(*) AS nb_lignes FROM orders
                             UNION ALL SELECT 'order_details', COUNT(*) FROM order_details
                             UNION ALL SELECT 'pizzas', COUNT(*) FROM pizzas
                             UNION ALL SELECT 'pizza_types', COUNT(*) FROM pizza_types""", con)
    st.dataframe(tailles, hide_index=True)
    st.caption("Une commande (orders) contient plusieurs lignes (order_details). Chaque ligne est une pizza "
               "d'une taille donnée (pizzas), qui appartient à un type de pizza (pizza_types).")

# =====================================================================
# RUBRIQUE 2 : le tableau de bord interactif
# =====================================================================
elif rubrique == "2. Tableau de bord":
    bandeau("📊 Tableau de bord", "Choisissez une période, une catégorie et une taille dans le menu de gauche.")

    # Filtres
    st.sidebar.header("Filtres")
    debut = st.sidebar.date_input("Du", datetime.date(2015, 1, 1))
    fin = st.sidebar.date_input("Au", datetime.date(2015, 12, 31))
    categories = pd.read_sql("SELECT DISTINCT category FROM pizza_types ORDER BY category", con)
    categorie = st.sidebar.selectbox("Catégorie", ["Toutes"] + categories["category"].tolist())
    taille = st.sidebar.selectbox("Taille", ["Toutes", "S", "M", "L", "XL", "XXL"])

    # Partie commune à toutes les requêtes : les ? sont remplacés dans l'ordre par les valeurs de parametres
    jointures = """
    FROM order_details
    JOIN orders ON order_details.order_id = orders.order_id
    JOIN pizzas ON order_details.pizza_id = pizzas.pizza_id
    JOIN pizza_types ON pizzas.pizza_type_id = pizza_types.pizza_type_id
    WHERE orders.date BETWEEN ? AND ?
    AND (? = 'Toutes' OR pizza_types.category = ?)
    AND (? = 'Toutes' OR pizzas.size = ?)
    """
    parametres = [str(debut), str(fin), categorie, categorie, taille, taille]

    def lire(debut_requete, fin_requete=""):
        """Lance une requête SQL avec les jointures et les filtres."""
        return pd.read_sql(debut_requete + jointures + fin_requete, con, params=parametres)

    # Indicateurs clés
    kpi = lire("""SELECT ROUND(SUM(order_details.quantity * pizzas.price), 2) AS chiffre_affaires,
                         COUNT(DISTINCT orders.order_id) AS nb_commandes,
                         SUM(order_details.quantity) AS pizzas_vendues""")
    if kpi["nb_commandes"][0] == 0:
        st.warning("Aucune vente pour ces filtres.")
        st.stop()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Chiffre d'affaires", kpi["chiffre_affaires"][0])
    col2.metric("🧾 Commandes", kpi["nb_commandes"][0])
    col3.metric("🍕 Pizzas vendues", kpi["pizzas_vendues"][0])
    col4.metric("🛒 Panier moyen", round(kpi["chiffre_affaires"][0] / kpi["nb_commandes"][0], 2))

    direction, planning, stock, marketing = st.tabs(
        ["📈 Direction", "👩‍🍳 Planning des équipes", "📦 Stock et achats", "📣 Marketing"])

    with direction:
        mois = lire("""SELECT strftime('%m', orders.date) AS mois,
                              ROUND(SUM(order_details.quantity * pizzas.price), 2) AS chiffre_affaires""",
                    "GROUP BY mois ORDER BY mois")
        fig = px.bar(mois, x="mois", y="chiffre_affaires", color_discrete_sequence=PALETTE,
                     title="Chiffre d'affaires par mois")
        fig.update_xaxes(type="category")   # affiche les 12 mois : 01, 02, 03...
        joli(fig)
        gauche, droite = st.columns(2)
        with gauche:
            cat = lire("""SELECT pizza_types.category AS categorie,
                                 ROUND(SUM(order_details.quantity * pizzas.price), 2) AS chiffre_affaires""",
                       "GROUP BY pizza_types.category")
            joli(px.pie(cat, names="categorie", values="chiffre_affaires", hole=0.4,
                        color_discrete_sequence=PALETTE, title="Part du CA par catégorie"))
        with droite:
            tai = lire("""SELECT pizzas.size AS taille,
                                 ROUND(SUM(order_details.quantity * pizzas.price), 2) AS chiffre_affaires""",
                       "GROUP BY pizzas.size")
            joli(px.pie(tai, names="taille", values="chiffre_affaires", hole=0.4,
                        color_discrete_sequence=PALETTE, title="Part du CA par taille"))

    with planning:
        jh = lire("""SELECT strftime('%w', orders.date) AS num_jour, strftime('%H', orders.time) AS heure,
                            COUNT(DISTINCT orders.order_id) AS nb_commandes""",
                  "GROUP BY num_jour, heure")
        tableau = jh.pivot(index="num_jour", columns="heure", values="nb_commandes").fillna(0)
        tableau.index = [JOURS[int(numero)] for numero in tableau.index]   # 0 -> dim, 1 -> lun...
        joli(px.imshow(tableau, color_continuous_scale="Oranges", aspect="auto",
                       labels=dict(x="Heure", y="Jour", color="Commandes"),
                       title="Commandes par jour et par heure (plus c'est foncé, plus il y a de monde)"))
        ph = lire("""SELECT orders.date, strftime('%H', orders.time) AS heure,
                            SUM(order_details.quantity) AS nb_pizzas""",
                  "GROUP BY orders.date, heure ORDER BY heure")
        joli(px.box(ph, x="heure", y="nb_pizzas", color_discrete_sequence=PALETTE,
                    title="Pizzas à préparer dans l'heure (une boîte = tous les jours de la période)"))

    with stock:
        ing = lire("SELECT pizza_types.ingredients, SUM(order_details.quantity) AS pizzas_vendues",
                   "GROUP BY pizza_types.ingredients")
        ing["ingredient"] = ing["ingredients"].str.split(", ")
        ing = ing.explode("ingredient")
        top_ing = ing.groupby("ingredient", as_index=False)["pizzas_vendues"].sum()
        nb = st.slider("Nombre d'ingrédients à afficher", 5, 30, 10)
        top_ing = top_ing.sort_values("pizzas_vendues", ascending=False).head(nb)
        fig = px.bar(top_ing, x="pizzas_vendues", y="ingredient", orientation="h",
                     color_discrete_sequence=PALETTE, title="Ingrédients présents dans le plus de pizzas vendues")
        fig.update_yaxes(autorange="reversed")
        joli(fig)
        piz = lire("""SELECT pizza_types.name AS pizza, pizza_types.category AS categorie,
                             SUM(order_details.quantity) AS pizzas_vendues,
                             ROUND(SUM(order_details.quantity * pizzas.price), 2) AS chiffre_affaires""",
                   "GROUP BY pizza_types.name")
        joli(px.scatter(piz, x="pizzas_vendues", y="chiffre_affaires", color="categorie", hover_name="pizza",
                        color_discrete_sequence=PALETTE,
                        title="Chaque point est une pizza (passez la souris pour voir son nom)"))
        st.write("Les 5 pizzas les moins vendues")
        st.dataframe(piz.sort_values("pizzas_vendues").head(5), hide_index=True)

    with marketing:
        gauche, droite = st.columns(2)
        with gauche:
            cmd = lire("SELECT orders.order_id, SUM(order_details.quantity) AS nb_pizzas", "GROUP BY orders.order_id")
            taille_cmd = cmd["nb_pizzas"].value_counts().sort_index().reset_index()
            taille_cmd.columns = ["nb_pizzas", "nb_commandes"]
            joli(px.bar(taille_cmd, x="nb_pizzas", y="nb_commandes", color_discrete_sequence=PALETTE,
                        title="Nombre de pizzas par commande"))
        with droite:
            jours = lire("""SELECT strftime('%w', orders.date) AS num_jour,
                                   ROUND(COUNT(DISTINCT orders.order_id) * 1.0 / COUNT(DISTINCT orders.date), 1) AS commandes_par_jour""",
                         "GROUP BY num_jour ORDER BY num_jour")
            jours["jour"] = [JOURS[int(numero)] for numero in jours["num_jour"]]
            joli(px.bar(jours, x="jour", y="commandes_par_jour", color_discrete_sequence=PALETTE,
                        title="Commandes par jour ouvert"))
        classement = st.radio("Classer les pizzas par", ["chiffre_affaires", "pizzas_vendues"], horizontal=True)
        meilleures = piz.sort_values(classement, ascending=False).head(10)
        fig = px.bar(meilleures, x=classement, y="pizza", orientation="h", color_discrete_sequence=PALETTE,
                     title="Top 10 des pizzas à mettre en avant")
        fig.update_yaxes(autorange="reversed")
        joli(fig)

# =====================================================================
# RUBRIQUE 3 : recommandations, conclusion et limites
# Chaque chiffre est recalculé ici par une requête SQL sur toute l'année.
# =====================================================================
else:
    bandeau("💡 Recommandations", "Ce que les données nous apprennent, et ce que Plato's Pizza pourrait essayer.")

    heure_pic = pd.read_sql("""SELECT strftime('%H', orders.time) AS heure, COUNT(orders.order_id) AS nb_commandes
                               FROM orders GROUP BY heure ORDER BY nb_commandes DESC LIMIT 1""", con)
    une_pizza = pd.read_sql("""SELECT ROUND(SUM(nb_pizzas = 1) * 100.0 / COUNT(*), 1) AS part
                               FROM (SELECT order_details.order_id, SUM(order_details.quantity) AS nb_pizzas
                                     FROM order_details GROUP BY order_details.order_id)""", con)
    grosses = pd.read_sql("""SELECT ROUND(SUM(CASE WHEN nb_pizzas >= 10 THEN montant ELSE 0 END) * 100.0 / SUM(montant), 1) AS part_ca
                             FROM (SELECT order_details.order_id, SUM(order_details.quantity) AS nb_pizzas,
                                          SUM(order_details.quantity * pizzas.price) AS montant
                                   FROM order_details JOIN pizzas ON order_details.pizza_id = pizzas.pizza_id
                                   GROUP BY order_details.order_id)""", con)
    derniere = pd.read_sql("""SELECT pizza_types.name, SUM(order_details.quantity) AS pizzas_vendues
                              FROM order_details
                              JOIN pizzas ON order_details.pizza_id = pizzas.pizza_id
                              JOIN pizza_types ON pizzas.pizza_type_id = pizza_types.pizza_type_id
                              GROUP BY pizza_types.name ORDER BY pizzas_vendues LIMIT 1""", con)

    st.header("Les constats clés")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⏰ Heure de pointe", heure_pic["heure"][0] + "h")
    col2.metric("🍕 Commandes à 1 pizza", f"{une_pizza['part'][0]} %")
    col3.metric("🎉 CA des commandes de 10+ pizzas", f"{grosses['part_ca'][0]} %")
    col4.metric("📉 Moins vendue", derniere["name"][0])

    st.header("Nos propositions")
    gauche, droite = st.columns(2)
    with gauche:
        carte("👩‍🍳 Planning", "Renforcer l'équipe le midi en semaine (12h-13h), et le soir le vendredi et le samedi. "
                              "Alléger l'après-midi (14h-16h), plus calme.")
        carte("📣 Marketing", "Beaucoup de commandes ne contiennent qu'une pizza : tester une offre duo ou un menu "
                             "pour augmenter le panier moyen.")
    with droite:
        carte("🎉 Commandes de groupe", "Les très grosses commandes pèsent plus lourd en CA qu'en nombre : "
                                       "proposer une offre groupe ou une précommande la veille.")
        carte("📦 Carte et stock", "Revoir les pizzas les moins vendues et les tailles XL et XXL. "
                                  "Sécuriser l'achat des ingrédients les plus utilisés.")

    st.header("Les limites")
    carte("⚠️ À garder en tête",
          "<ul><li>Une seule année de données (2015) : impossible de vérifier si les tendances se répètent.</li>"
          "<li>Pas de coûts, donc pas de marge : une pizza qui rapporte beaucoup n'est pas forcément rentable.</li>"
          "<li>Pas d'identifiant client ni de canal de vente (sur place, à emporter, livraison).</li>"
          "<li>La monnaie n'est pas précisée, et la liste d'ingrédients ne donne pas les quantités.</li>"
          "<li>Des jours sans commande (fermetures probables) dans l'année.</li></ul>")

con.close()
