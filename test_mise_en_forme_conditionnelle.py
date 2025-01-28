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

# Fonction pour générer une couleur en fonction de la valeur (coolwarm)
def get_coolwarm_color(value):
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = plt.get_cmap("coolwarm")
    return mcolors.rgb2hex(cmap(norm(value)))

# Générer les couleurs pour les colonnes "Centile"
color_mapping = {}
for col in df.columns:
    if col.startswith("Centile"):
        color_mapping[col] = {val: get_coolwarm_color(val) for val in df[col].unique()}

# Construire les GridOptions pour AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# Appliquer les styles conditionnels en JavaScript
for col in df.columns:
    if col.startswith("Centile"):
        js_code = f"""
        function(params) {{
            var colorMapping = {color_mapping[col]};
            return {{
                'backgroundColor': colorMapping[params.value] || 'white',
                'color': 'black'
            }};
        }}
        """
        gb.configure_column(col, cellStyle=js_code)

# Construire les options
grid_options = gb.build()

# Afficher la table dans Streamlit
AgGrid(df, gridOptions=grid_options)
