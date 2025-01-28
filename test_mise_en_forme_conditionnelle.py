import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Exemple de DataFrame avec des colonnes "Centile"
data = {
    "Nom": ["Alice", "Bob", "Charlie"],
    "Centile_A": [10, 50, 90],
    "Centile_B": [20, 70, 30],
    "Autre_Colonne": [1, 2, 3],
}
df = pd.DataFrame(data)

# Générer une fonction pour récupérer le dégradé coolwarm sous forme hexadécimale
def get_coolwarm_color(value):
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = plt.get_cmap("coolwarm")
    return mcolors.rgb2hex(cmap(norm(value)))

# Créer une colonne supplémentaire avec les couleurs pour les colonnes "Centile"
for col in df.columns:
    if col.startswith("Centile"):
        df[f"{col}_color"] = df[col].apply(get_coolwarm_color)

# Construire les GridOptions pour AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# Appliquer des styles conditionnels sur les colonnes "Centile"
for col in df.columns:
    if col.startswith("Centile"):
        gb.configure_column(
            col,
            cellStyle=lambda params: {
                "backgroundColor": params["data"][f"{col}_color"],
                "color": "black",
            },
        )

# Construire les options de la grille
grid_options = gb.build()

# Supprimer les colonnes "_color" de l'affichage
df = df[[col for col in df.columns if not col.endswith("_color")]]

# Afficher la table dans Streamlit
AgGrid(df, gridOptions=grid_options)
