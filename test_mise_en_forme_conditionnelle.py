import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# --- 📌 1. Création d'un DataFrame ---
data = {
    "Nom": ["Alice", "Bob", "Charlie"],
    "Centile_A": [10, 50, 90],
    "Centile_B": [20, 70, 30],
    "Autre_Colonne": [1, 2, 3],
}
df = pd.DataFrame(data)

# --- 📌 2. Fonction pour générer les couleurs Coolwarm ---
def get_coolwarm_color(value):
    norm = mcolors.Normalize(vmin=0, vmax=100)  # Normalisation entre 0 et 100
    cmap = plt.get_cmap("coolwarm")  # Palette coolwarm
    return mcolors.rgb2hex(cmap(norm(value)))  # Conversion en couleur hexadécimale

# --- 📌 3. Ajout d'une colonne cachée contenant les couleurs ---
for col in df.columns:
    if col.startswith("Centile"):
        df[f"{col}_color"] = df[col].apply(get_coolwarm_color)

# --- 📌 4. Configuration d'AgGrid ---
gb = GridOptionsBuilder.from_dataframe(df)

# --- 📌 5. Ajout du style conditionnel JSON (statique, sans lambda) ---
for col in df.columns:
    if col.startswith("Centile"):
        gb.configure_column(
            col,
            cellStyle={"function": "params => ({ backgroundColor: params.data['" + col + "_color'] })"},
        )

# --- 📌 6. Construire les options de la table ---
grid_options = gb.build()

# --- 📌 7. Supprimer les colonnes "_color" avant affichage ---
df = df[[col for col in df.columns if not col.endswith("_color")]]

# --- 📌 8. Afficher le tableau interactif ---
AgGrid(df, gridOptions=grid_options)
