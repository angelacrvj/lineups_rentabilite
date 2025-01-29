import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 📌 Titre de l'application
st.title("Test de mise en forme conditionnelle avec AgGrid 🎨")

# 📌 Générer un DataFrame d'exemple
data = {
    "Nom": ["Alice", "Bob", "Charlie", "David", "Emma"],
    "Centile_A": [10, 50, 90, 30, 70],
    "Centile_B": [20, 70, 30, 90, 50],
    "Score": [3, 5, 8, 2, 7],  # Une colonne normale pour comparaison
}
df = pd.DataFrame(data)

# 📌 Fonction pour récupérer une couleur du dégradé "coolwarm"
def get_color(value):
    """Renvoie un code hexadécimal pour une valeur entre 0 et 100 en utilisant le cmap coolwarm."""
    norm = mcolors.Normalize(vmin=0, vmax=100)
    cmap = plt.get_cmap("coolwarm")
    color = mcolors.rgb2hex(cmap(norm(value)))
    return color

# 📌 Fonction de style conditionnel appliqué aux colonnes "Centile"
def get_cell_styles(df):
    """Génère les styles de cellules pour les colonnes Centile."""
    styles = []
    for index, row in df.iterrows():
        for col in df.columns:
            if col.startswith("Centile"):
                color = get_color(row[col])  # Obtenir la couleur associée à la valeur
                styles.append({
                    "if": {"rowIndex": index, "columnId": col},
                    "backgroundColor": color,
                    "color": "black",
                })
    return styles

# 📌 Configuration de la table AgGrid
gb = GridOptionsBuilder.from_dataframe(df)

# Activer les options interactives
gb.configure_default_column(editable=False, groupable=True)

# Définir les styles conditionnels
grid_options = gb.build()
grid_options["getRowStyle"] = get_cell_styles(df)  # Appliquer le style

# 📌 Affichage de la table avec AgGrid
st.subheader("📊 Tableau avec mise en forme conditionnelle")
AgGrid(df, gridOptions=grid_options, enable_enterprise_modules=False, theme="streamlit")

# 📌 Légende pour la compréhension du dégradé
st.subheader("🎨 Légende du dégradé coolwarm")
gradient = plt.figure(figsize=(6, 1))
ax = gradient.add_axes([0, 0, 1, 0.3])

# Création d'un dégradé horizontal
cmap = plt.get_cmap("coolwarm")
norm = mcolors.Normalize(vmin=0, vmax=100)
cb = plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax, orientation='horizontal')
cb.set_label("Valeurs des centiles (0 à 100)")

# Afficher la légende sous forme d'image
st.pyplot(gradient)
