import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# --- 📌 1. Créer un DataFrame avec des colonnes "Centile" ---
data = {
    "Nom": ["Alice", "Bob", "Charlie"],
    "Centile_A": [10, 50, 90],
    "Centile_B": [20, 70, 30],
    "Autre_Colonne": [1, 2, 3],
}
df = pd.DataFrame(data)

# --- 📌 2. Générer une fonction pour récupérer une couleur "coolwarm" ---
def get_coolwarm_color(value):
    norm = mcolors.Normalize(vmin=0, vmax=100)  # Normalisation de 0 à 100
    cmap = plt.get_cmap("coolwarm")  # Palette coolwarm
    return mcolors.rgb2hex(cmap(norm(value)))  # Conversion en couleur hexadécimale

# --- 📌 3. Configurer AgGrid ---
gb = GridOptionsBuilder.from_dataframe(df)

# 📌 --- 4. Appliquer la mise en forme conditionnelle sur les colonnes "Centile" ---
for col in df.columns:
    if col.startswith("Centile"):  # Sélectionner uniquement les colonnes Centile
        gb.configure_column(
            col,
            cellStyle=lambda params: {
                "backgroundColor": get_coolwarm_color(params["value"]),
                "color": "black",
                "textAlign": "center",
            },
        )

# 📌 --- 5. Construire les options de la table ---
grid_options = gb.build()

# 📌 --- 6. Afficher la table dans Streamlit ---
AgGrid(df, gridOptions=grid_options)
