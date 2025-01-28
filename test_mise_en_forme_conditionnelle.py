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

# Générer une fonction pour appliquer le dégradé "coolwarm" à une valeur entre 0 et 100
def get_color(value):
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = plt.get_cmap("coolwarm")  # Dégradé coolwarm
    color = mcolors.rgb2hex(cmap(norm(value)))  # Convertir en code hexadécimal
    return color

# Fonction de style conditionnel pour les colonnes "Centile"
def cell_style(params):
    if "Centile" in params["colDef"]["field"]:  # Vérifier si la colonne commence par "Centile"
        color = get_color(params["value"])
        return {"backgroundColor": color, "color": "black"}  # Appliquer la couleur
    return None

# Configurer la table AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# Appliquer la fonction de style conditionnel à toutes les colonnes
gb.configure_columns(
    [col for col in df.columns if col.startswith("Centile")],  # Colonnes ciblées
    cellStyle=cell_style,  # Fonction de style conditionnel
)

# Construire les options de configuration
grid_options = gb.build()

# Afficher la table avec AgGrid
AgGrid(df, gridOptions=grid_options)
