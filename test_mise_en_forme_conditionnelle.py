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

# Ajouter une colonne "color" cachée pour chaque colonne Centile
for col in df.columns:
    if col.startswith("Centile"):
        df[f"{col}_color"] = df[col].apply(get_coolwarm_color)

# Configurer AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# Ajouter des règles CSS basées sur la couleur stockée dans "_color"
for col in df.columns:
    if col.startswith("Centile"):
        gb.configure_column(
            col,
            cellClassRules={
                f"bg-{col.lower()}": "true"
            },
        )

# Construire les options de la grille
grid_options = gb.build()

# Supprimer les colonnes "_color" de l'affichage
df = df[[col for col in df.columns if not col.endswith("_color")]]

# Générer le CSS dynamique pour les couleurs
custom_css = "<style>\n"
for col in df.columns:
    if col.startswith("Centile"):
        for value in df[col].unique():
            color = get_coolwarm_color(value)
            class_name = f"bg-{col.lower()}"
            custom_css += f"""
            .ag-theme-streamlit .{class_name} {{
                background-color: {color} !important;
                color: black !important;
            }}
            """
custom_css += "</style>"

# Injecter le CSS dans Streamlit
st.markdown(custom_css, unsafe_allow_html=True)

# Afficher le tableau interactif
AgGrid(df, gridOptions=grid_options)
